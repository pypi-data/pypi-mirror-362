"""
Endpoints for API indexing from Dashboard and Git Hooks.
NOT for direct user use.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
from pathlib import Path
import time
import re
import os

# Core imports
from acolyte.core.logging import logger
from acolyte.core.id_generator import generate_id
from acolyte.core.secure_config import Settings
from acolyte.core.utils.file_types import FileTypeDetector
from acolyte.core.exceptions import (
    ValidationError,
    ConfigurationError,
    from_exception,
    internal_error,
)

# Services imports
from acolyte.services import IndexingService
from acolyte.core.progress import progress_tracker
from acolyte.core.progress.tracker import TaskStatus

# NOTE: The progress is notified automatically via EventBus
# IndexingService publishes ProgressEvent → WebSocket listens to it
# No manual notify_progress() is required

router = APIRouter()

# Configuration
config = Settings()
logger.info("Indexing API initializing...", module="index")


# ============================================================================
# DOCKER DETECTION
# ============================================================================


def is_running_in_docker() -> bool:
    """Check if running inside Docker container."""
    return os.path.exists('/.dockerenv') or os.getenv('RUNNING_IN_DOCKER') == 'true'


# ============================================================================
# MODELS FOR REQUEST/RESPONSE
# ============================================================================


class ProjectIndexRequest(BaseModel):
    """Request for initial indexing from dashboard."""

    patterns: List[str] = Field(
        default_factory=lambda: _get_default_patterns(),
        description="File patterns to index",
    )
    exclude_patterns: List[str] = Field(
        default=["**/node_modules/**", "**/__pycache__/**", "**/dist/**", "**/.git/**"],
        description="File patterns to exclude",
    )
    respect_gitignore: bool = Field(default=True, description="Respect .gitignore rules")
    respect_acolyteignore: bool = Field(default=True, description="Respect .acolyteignore rules")
    force_reindex: bool = Field(default=False, description="Force re-indexing of existing files")

    # 🔧 CRITICAL FIX: Add project_path field to allow specifying which project to index
    project_path: Optional[str] = Field(
        None, description="Path to the project to index (overrides default)"
    )
    resume_task_id: Optional[str] = Field(
        None, description="Task ID to resume from previous indexing"
    )

    @field_validator("patterns")
    @classmethod
    def validate_patterns(cls, v):
        if not v:
            raise ValueError("At least one pattern required")
        if len(v) > 50:
            raise ValueError("Too many patterns (max 50)")
        return v

    @field_validator("exclude_patterns")
    @classmethod
    def validate_exclude_patterns(cls, v):
        if len(v) > 100:
            raise ValueError("Too many exclude patterns (max 100)")
        return v


class GitChangeFile(BaseModel):
    """Information about a modified file in Git."""

    path: str = Field(..., description="Relative path of the file")
    action: str = Field(..., description="Action: added, modified, deleted, renamed")
    old_path: Optional[str] = Field(None, description="Previous path (only for renamed)")
    diff: Optional[str] = Field(None, description="Diff of the file (optional)")

    @field_validator("action")
    @classmethod
    def validate_action(cls, v):
        valid_actions = {"added", "modified", "deleted", "renamed"}
        if v not in valid_actions:
            raise ValueError(f"Invalid action: {v}. Must be one of: {valid_actions}")
        return v

    @field_validator("path")
    @classmethod
    def validate_path(cls, v):
        if not v or not v.strip():
            raise ValueError("Path cannot be empty")

        # Improved security validation with pathlib
        from pathlib import Path

        try:
            # Normalize and resolve the path (without base yet)
            path_str = v.strip()

            # Reject absolute paths or paths with dangerous characters
            if path_str.startswith(("/", "\\")) or ".." in path_str:
                logger.info("[TRACE] GitChangeFile path validation: absolute or parent refs")
                raise ValueError("Path cannot be absolute or contain parent directory references")

            # Reject paths with problematic Windows characters
            if any(char in path_str for char in [":", "*", "?", '"', "<", ">", "|"]) and not (
                len(path_str) > 1 and path_str[1] == ":"
            ):
                logger.info("[TRACE] GitChangeFile path validation: invalid characters")
                raise ValueError("Path contains invalid characters")

            # Try to create a Path to validate format
            test_path = Path(path_str)

            # Reject if it has absolute components or parent
            if test_path.is_absolute() or any(part == ".." for part in test_path.parts):
                logger.info("[TRACE] GitChangeFile path validation: absolute components")
                raise ValueError("Path must be relative and cannot navigate to parent directories")

            return path_str

        except (ValueError, OSError) as e:
            # Re-throw ValueError with clearer message
            if isinstance(e, ValueError):
                raise e
            logger.info("[TRACE] GitChangeFile path validation: OSError")
            raise ValueError(f"Invalid path format: {str(e)}")
        except Exception:
            logger.info("[TRACE] GitChangeFile path validation: general exception")
            raise ValueError("Invalid path format")


class GitChangesRequest(BaseModel):
    """Request from git hooks after commit."""

    trigger: str = Field(..., description="Trigger type: commit, pull, checkout, fetch")
    files: List[GitChangeFile] = Field(..., description="List of modified files")

    # Metadata of the commit (optional)
    commit_hash: Optional[str] = Field(None, description="Hash of the commit")
    branch: Optional[str] = Field(None, description="Current branch")
    author: Optional[str] = Field(None, description="Author of the commit")
    message: Optional[str] = Field(None, description="Message of the commit")
    timestamp: Optional[int] = Field(None, description="Timestamp of the commit")

    # Metadata specific to the trigger
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("trigger")
    @classmethod
    def validate_trigger(cls, v):
        valid_triggers = {"commit", "pull", "checkout", "fetch"}
        if v not in valid_triggers:
            raise ValueError(f"Invalid trigger: {v}. Must be one of: {valid_triggers}")
        return v

    @field_validator("files")
    @classmethod
    def validate_files(cls, v):
        if not v:
            logger.info("[TRACE] GitChangesRequest.validate_files: empty list")
            raise ValueError("At least one file change required")
        if len(v) > 1000:
            logger.info("[TRACE] GitChangesRequest.validate_files: too many files")
            raise ValueError("Too many file changes (max 1000)")
        return v


# ============================================================================
# ENDPOINTS
# ============================================================================


@router.post("/project")
async def index_project(
    request: ProjectIndexRequest, background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Initial indexing of the entire project.

    Called by:
    - Dashboard web during initial setup
    - CLI command `acolyte index` in emergencies

    IMPORTANT: It can take several minutes to index large projects.
    Use WebSocket /api/ws/progress/{task_id} to see progress.

    Supports resuming from previous interrupted indexing tasks by providing
    resume_task_id from a previous indexing operation.
    """
    start_time = time.time()
    task_id = f"idx_{int(time.time())}_{generate_id()[:8]}"

    logger.info(
        "Project index request",
        patterns_count=len(request.patterns),
        force_reindex=request.force_reindex,
        task_id=task_id,
        resume_from=request.resume_task_id,
    )

    try:
        # IndexingService handles concurrency internally with _indexing_lock
        # If there is indexing in progress, index_files() will automatically throw an exception

        # Get the root of the project safely
        try:
            # 🔧 SIMPLIFIED: Use /project directly when in Docker
            if is_running_in_docker():
                project_root = Path("/project")
                logger.info("🔍 DOCKER: Using /project as root")

                # Validate that /project exists
                if not project_root.exists():
                    logger.error("🔍 DOCKER: /project does not exist!")
                    raise ConfigurationError(
                        message="Docker project mount not found: /project",
                        context={"docker_detected": True, "expected_path": "/project"},
                    )
            else:
                # Not in Docker - use provided path or fallback
                project_root_path = (
                    request.project_path
                    or os.getenv("ACOLYTE_PROJECT_ROOT")
                    or config.get("project.path", ".")
                )
                project_root = Path(project_root_path).resolve()

                if not project_root.exists():
                    raise ConfigurationError(
                        message=f"Project root does not exist: {project_root}",
                        context={"configured_path": project_root_path},
                    )

            logger.info(f"🔍 DEBUG: Final project_root: {project_root}")
            logger.info(f"🔍 DEBUG: Root exists: {project_root.exists()}")
            logger.info(f"🔍 DEBUG: Root is dir: {project_root.is_dir()}")
        except Exception as e:
            logger.error(f"🔍 ERROR: Exception in project root determination: {e}")
            raise ConfigurationError(
                message="Invalid project root configuration", context={"error": str(e)}
            )

        # Estimate files without full scan
        # This is just an approximation for user feedback
        estimated_files = await _estimate_without_full_scan(project_root, request.patterns)

        # Calculate estimated time (approx 0.1s per file)
        estimated_seconds = max(estimated_files * 0.1, 5)  # Minimum 5 seconds

        # Collect files to index ONCE here
        files_to_index = await _collect_files_to_index(
            project_root, request.patterns, request.exclude_patterns or []
        )

        # Update estimated files with actual count
        estimated_files = len(files_to_index)

        # Register task in progress tracker
        progress_tracker.start_task(
            task_id=task_id, total=estimated_files, message="Initializing indexing service..."
        )

        # Start asynchronous indexing
        background_tasks.add_task(
            _run_project_indexing,
            task_id=task_id,
            files_to_index=files_to_index,  # Pass the already collected files
            request=request,
            estimated_files=estimated_files,
        )

        processing_time = int((time.time() - start_time) * 1000)

        logger.info(
            "Project index started",
            task_id=task_id,
            estimated_files=estimated_files,
            processing_time_ms=processing_time,
        )

        response = {
            "task_id": task_id,
            "status": "started",
            "estimated_files": estimated_files,
            "estimated_seconds": int(estimated_seconds),
            "websocket_url": f"/api/ws/progress/{task_id}",
            "project_root": str(project_root),
            "patterns": request.patterns,
            "message": "Project indexing started. Connect to WebSocket for real-time progress.",
        }

        # Include resume information if applicable
        if request.resume_task_id:
            response["resumed_from"] = request.resume_task_id
            response["message"] = (
                f"Project indexing resumed from task {request.resume_task_id}. Connect to WebSocket for real-time progress."
            )

        return response

    except (ValidationError, ConfigurationError) as e:
        logger.warning(
            "Project index validation failed", validation_message=e.message, task_id=task_id
        )
        logger.info("[TRACE] index_project validation/config error")
        raise HTTPException(status_code=400, detail=from_exception(e).model_dump())

    except Exception as e:
        logger.error("Project index failed", error=str(e), task_id=task_id, exc_info=True)
        error_response = internal_error(
            message="Failed to start project indexing",
            error_id=task_id,
            context={"error_type": type(e).__name__},
        )
        raise HTTPException(status_code=500, detail=error_response.model_dump())


@router.get("/project/status/{task_id}")
async def get_indexing_status(task_id: str) -> Dict[str, Any]:
    """
    Get current status of an indexing task.
    Returns immediately with current state or 404 if not found.
    """
    task_info = progress_tracker.get_task(task_id)

    if not task_info:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_info.to_dict()


@router.get("/project/tasks")
async def get_active_tasks() -> Dict[str, Any]:
    """
    Get all active indexing tasks.
    """
    active_tasks = progress_tracker.get_active_tasks()
    return {"tasks": [task.to_dict() for task in active_tasks], "count": len(active_tasks)}


@router.post("/git-changes")
async def index_git_changes(
    request: GitChangesRequest, background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """
    Index changes after a Git commit.

    Called automatically by git hooks (post-commit, post-merge, etc.).
    Processes only modified files, not the entire project.

    IMPORTANT: This endpoint is fast (only processes diffs).
    """
    start_time = time.time()
    request_id = generate_id()[:8]

    logger.info(
        "Git changes request",
        trigger=request.trigger,
        files_count=len(request.files),
        request_id=request_id,
    )

    try:
        # Get the root of the project
        project_root_path = os.getenv("ACOLYTE_PROJECT_ROOT", config.get("project.path", "."))
        project_root = Path(project_root_path).resolve()

        processed_files = []
        skipped_files = []
        error_files = []

        # Process each file
        for file_change in request.files:
            try:
                result = await _process_file_change(
                    project_root=project_root,
                    file_change=file_change,
                    trigger=request.trigger,
                    commit_metadata={
                        "hash": request.commit_hash,
                        "author": request.author,
                        "message": request.message,
                        "timestamp": request.timestamp,
                        "branch": request.branch,
                    },
                )

                if result["status"] == "processed":
                    processed_files.append(result)
                elif result["status"] == "skipped":
                    skipped_files.append(result)

            except Exception as e:
                logger.error("Error processing file", path=file_change.path, error=str(e))
                error_files.append(
                    {
                        "file": file_change.path,
                        "action": file_change.action,
                        "error": str(e),
                        "error_type": type(e).__name__,
                    }
                )

        # Apply cache invalidation if necessary
        if request.trigger in ["pull", "checkout"] and processed_files:
            try:
                # The cache invalidation is handled automatically by the EventBus
                # The services subscribe to CacheInvalidateEvent as needed
                logger.info("Cache invalidation triggered", files_count=len(processed_files))
            except Exception as e:
                logger.warning("Cache invalidation failed", error=str(e))

        processing_time = int((time.time() - start_time) * 1000)

        # Determine the general state
        total_files = len(request.files)
        success_rate = len(processed_files) / total_files if total_files > 0 else 0

        status = "success"
        if error_files:
            status = "partial_success" if processed_files else "failed"

        result = {
            "status": status,
            "trigger": request.trigger,
            "processing_time_ms": processing_time,
            "summary": {
                "total_files": total_files,
                "processed": len(processed_files),
                "skipped": len(skipped_files),
                "errors": len(error_files),
                "success_rate": round(success_rate, 2),
            },
            "details": {
                "processed_files": processed_files[:20],  # First 20
                "skipped_files": skipped_files[:10],  # First 10
                "error_files": error_files[:10],  # First 10
            },
        }

        # Add commit metadata if available
        if request.commit_hash:
            result["commit"] = {
                "hash": request.commit_hash[:8],
                "branch": request.branch,
                "author": request.author,
                "message": request.message[:100] if request.message else None,
            }

        logger.info(
            "Git changes processed",
            status=status,
            processed_count=len(processed_files),
            total_files=total_files,
            processing_time_ms=processing_time,
            request_id=request_id,
        )

        return result

    except Exception as e:
        logger.error("Git changes failed", error=str(e), request_id=request_id, exc_info=True)
        error_response = internal_error(
            message="Failed to process git changes",
            error_id=request_id,
            context={
                "error_type": type(e).__name__,
                "trigger": request.trigger,
                "files_count": len(request.files),
            },
        )
        raise HTTPException(status_code=500, detail=error_response.model_dump())


# NOTE: Endpoint /cache removed - over-engineering unnecessary
# Orphaned embeddings are a theoretical problem that doesn't happen in practice


# ============================================================================
# FASE 3: ENDPOINTS DE CONTROL AVANZADO PARA BATCH PROCESSING
# ============================================================================


@router.post("/batch/pause/{task_id}")
async def pause_batch_processing(task_id: str) -> Dict[str, Any]:
    """
    Pausar procesamiento de batch entre batches.

    FASE 3: Control avanzado que permite pausar la indexación durante
    el procesamiento por batches. La pausa ocurre entre batches, no
    durante el procesamiento de un batch individual.
    """
    try:
        # Verificar que la tarea existe
        task_info = progress_tracker.get_task(task_id)
        if not task_info:
            raise HTTPException(status_code=404, detail="Task not found")

        # Verificar que la tarea está en progreso
        if task_info.status != TaskStatus.RUNNING:
            raise HTTPException(
                status_code=400, detail=f"Cannot pause task in status: {task_info.status.value}"
            )

        # Marcar para pausa usando el progress tracker (thread-safe)
        # El IndexingService verificará esto entre batches

        # Actualizar el task info con información de pausa (no cambiar status)
        # Mantener el status actual ya que pausar no es lo mismo que cancelar
        progress_tracker.update_task(
            task_id,
            message="Pausing after current batch...",
            stats={"pause_requested": True, "is_paused": True},
            # No establecer status=TaskStatus.CANCELLED para evitar confusión semántica
        )

        logger.info("Batch processing pause requested", task_id=task_id)

        return {
            "status": "pause_requested",
            "task_id": task_id,
            "message": "Batch processing will pause after current batch completes",
            "current_status": task_info.status.value,
            "current_progress": f"{task_info.current}/{task_info.total}",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to pause batch processing", task_id=task_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/batch/resume/{task_id}")
async def resume_batch_processing(task_id: str) -> Dict[str, Any]:
    """
    Reanudar procesamiento de batch desde checkpoint.

    FASE 3: Permite reanudar indexación pausada o usar checkpoints
    guardados para recuperación after failures.
    """
    try:
        # Verificar que la tarea existe
        task_info = progress_tracker.get_task(task_id)
        if not task_info:
            raise HTTPException(status_code=404, detail="Task not found")

        # Quitar de la lista de pausados
        # Estado de pausa ahora se maneja en el progress tracker

        # Si la tarea estaba pausada, reanudar (verificar por stats, no por status)
        if task_info.stats.get("is_paused", False):
            progress_tracker.update_task(
                task_id,
                message="Resuming batch processing...",
                stats={"resumed": True, "is_paused": False},
                # Mantener el status actual, no cambiarlo a RUNNING necesariamente
            )

        logger.info("Batch processing resumed", task_id=task_id)

        return {
            "status": "resumed",
            "task_id": task_id,
            "message": "Batch processing resumed",
            "current_status": task_info.status.value,
            "current_progress": f"{task_info.current}/{task_info.total}",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to resume batch processing", task_id=task_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/batch/stats/{task_id}")
async def get_batch_stats(task_id: str) -> Dict[str, Any]:
    """
    Obtener estadísticas detalladas del batch processing.

    FASE 3: Estadísticas avanzadas que incluyen información de
    batches, performance metrics, y proyecciones de tiempo.
    """
    try:
        # Obtener información de la tarea
        task_info = progress_tracker.get_task(task_id)
        if not task_info:
            raise HTTPException(status_code=404, detail="Task not found")

        # Estadísticas básicas
        basic_stats = task_info.to_dict()

        # Estadísticas específicas de batch (si están disponibles)
        batch_stats = {}
        if task_info.stats:
            # Extraer información de batch de los stats
            for key, value in task_info.stats.items():
                if 'batch' in key.lower():
                    batch_stats[key] = value

        # Calcular métricas de performance
        elapsed_time = time.time() - task_info.started_at
        if elapsed_time > 0 and task_info.current > 0:
            files_per_second = task_info.current / elapsed_time
            estimated_total_time = (task_info.total / task_info.current) * elapsed_time
            estimated_remaining = max(0, estimated_total_time - elapsed_time)
        else:
            files_per_second = 0
            estimated_total_time = 0
            estimated_remaining = 0

        # Información de pausa si aplica
        is_paused = task_info.stats.get("is_paused", False)

        return {
            **basic_stats,
            "batch_info": batch_stats,
            "performance_metrics": {
                "files_per_second": round(files_per_second, 2),
                "estimated_remaining_seconds": round(estimated_remaining, 0),
                "estimated_remaining_minutes": round(estimated_remaining / 60, 1),
                "elapsed_time_seconds": round(elapsed_time, 1),
            },
            "control_info": {
                "is_paused": is_paused,
                "can_pause": task_info.status == TaskStatus.RUNNING,
                "can_resume": is_paused
                or task_info.status in [TaskStatus.CANCELLED, TaskStatus.FAILED],
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get batch stats", task_id=task_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/system/memory")
async def get_memory_stats() -> Dict[str, Any]:
    """
    🔧 NEW: Obtener estadísticas de memoria del sistema de tracking.

    Endpoint para monitorear memory leaks y estado del ProgressTracker.
    Útil para debugging y monitoring de producción.
    """
    try:
        # Obtener estadísticas de memoria del ProgressTracker
        memory_stats = progress_tracker.get_memory_stats()

        # Añadir información del sistema si está disponible
        import psutil

        process = psutil.Process()
        system_stats = {
            "process_memory_mb": round(process.memory_info().rss / 1024 / 1024, 1),
            "process_cpu_percent": process.cpu_percent(),
            "system_memory_percent": psutil.virtual_memory().percent,
        }
    except ImportError:
        # psutil no disponible, solo estadísticas internas
        system_stats = {
            "process_memory_mb": "unavailable (psutil not installed)",
            "process_cpu_percent": "unavailable",
            "system_memory_percent": "unavailable",
        }
    except Exception as e:
        logger.warning("Failed to get system stats", error=str(e))
        system_stats = {
            "process_memory_mb": f"error: {str(e)}",
            "process_cpu_percent": "error",
            "system_memory_percent": "error",
        }

    return {
        "progress_tracker": memory_stats,
        "system": system_stats,
        "timestamp": time.time(),
        "memory_health": {
            "status": (
                "healthy"
                if memory_stats["total_tasks"] < 500
                else "warning" if memory_stats["total_tasks"] < 800 else "critical"
            ),
            "recommendations": _get_memory_recommendations(memory_stats),
        },
    }


def _get_memory_recommendations(stats: Dict[str, Any]) -> List[str]:
    """Generar recomendaciones basadas en estadísticas de memoria."""
    recommendations = []

    total_tasks = stats.get("total_tasks", 0)
    oldest_age = stats.get("oldest_task_age_hours", 0)

    if total_tasks > 800:
        recommendations.append("High task count detected - consider increasing cleanup frequency")

    if oldest_age > 24:
        recommendations.append(
            f"Very old task detected ({oldest_age:.1f}h) - investigate abandoned tasks"
        )

    status_breakdown = stats.get("status_breakdown", {})
    running_tasks = status_breakdown.get("running", 0)
    if running_tasks > 50:
        recommendations.append(f"Many running tasks ({running_tasks}) - check for stuck operations")

    if not recommendations:
        recommendations.append("Memory usage looks healthy")

    return recommendations


# Helper function para que IndexingService pueda verificar pausas
def is_task_paused(task_id: str) -> bool:
    """
    Verificar si una tarea ha sido pausada externamente.
    FASE 3: Usado por IndexingService para verificar pausas entre batches.
    """
    task_info = progress_tracker.get_task(task_id)
    if not task_info:
        return False
    return task_info.stats.get("is_paused", False)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_default_patterns() -> List[str]:
    """Get default file patterns from FileTypeDetector."""
    # Get all supported extensions
    extensions = FileTypeDetector.get_all_supported_extensions()
    # Convert to glob patterns (add * prefix)
    patterns = [f"*{ext}" for ext in sorted(extensions)]
    # Return most common ones first
    priority_patterns = ["*.py", "*.js", "*.ts", "*.tsx", "*.md", "*.yml", "*.yaml"]
    other_patterns = [p for p in patterns if p not in priority_patterns]
    return priority_patterns + other_patterns[:10]  # Limit to avoid too many patterns


def _glob_to_regex(pattern: str) -> re.Pattern:
    """
    Convert glob pattern to regex with proper support for:
    - ** (recursive directory matching)
    - * (single level wildcard)
    - ? (single character)
    - [chars] and [!chars] (character sets)
    """
    # Escape special regex characters (except glob characters)
    pattern = re.escape(pattern)

    # Now unescape and convert glob patterns
    # Order matters: handle ** before *
    pattern = pattern.replace(r'\*\*', '.*')  # ** matches everything
    pattern = pattern.replace(r'\*', '[^/]*')  # * matches anything except /
    pattern = pattern.replace(r'\?', '.')  # ? matches single char

    # Handle character sets [abc] and [!abc]
    pattern = re.sub(r'\\\[([^\]]+)\\\]', r'[\1]', pattern)
    pattern = pattern.replace('[!', '[^')  # [!abc] -> [^abc]

    # For exclude patterns, we want to match anywhere in the path
    # Don't anchor with ^ and $ for exclude patterns
    return re.compile(pattern)


async def _collect_files_to_index(
    root: Path, patterns: List[str], exclude_patterns: Optional[List[str]] = None
) -> List[str]:
    """
    Collect all files to index based on patterns, applying exclude_patterns.
    """
    try:
        # 🔍 DEBUG: Show exactly where we're searching
        logger.info(f"🔍 DEBUG: _collect_files_to_index called with root={root}")
        logger.info(f"🔍 DEBUG: Root path type: {type(root)}")
        logger.info(f"🔍 DEBUG: Root path exists: {root.exists()}")
        logger.info(f"🔍 DEBUG: Root path is dir: {root.is_dir()}")
        logger.info(f"🔍 DEBUG: Root path absolute: {root.resolve()}")

        # Show what's actually in the root directory
        if root.exists() and root.is_dir():
            items = list(root.iterdir())
            logger.info(f"🔍 DEBUG: Root directory contains {len(items)} items:")
            for item in items[:10]:  # Show first 10 items
                logger.info(f"🔍 DEBUG: - {item.name} ({'dir' if item.is_dir() else 'file'})")

            # Quick test - count Python files manually
            py_files = list(root.rglob("*.py"))
            logger.info(f"🔍 DEBUG: Manual count of *.py files: {len(py_files)}")

            # Show first few Python files found
            for py_file in py_files[:5]:
                logger.info(f"🔍 DEBUG: Found Python file: {py_file}")
        else:
            logger.error("🔍 DEBUG: Root directory does not exist or is not a directory!")
            logger.error(f"🔍 DEBUG: Current working directory: {os.getcwd()}")
            logger.error(
                f"🔍 DEBUG: ACOLYTE_PROJECT_ROOT env var: {os.getenv('ACOLYTE_PROJECT_ROOT', 'not set')}"
            )

        files_to_index = []
        exclude_patterns = exclude_patterns or []
        exclude_regexes = [_glob_to_regex(p) for p in exclude_patterns]

        logger.info(
            "🔍 DEBUG: Starting file collection",
            root=str(root),
            patterns=patterns,
            exclude_patterns=exclude_patterns,
            exclude_regexes_count=len(exclude_regexes),
        )

        # Log exclude regexes for debugging
        for i, regex in enumerate(exclude_regexes):
            logger.info(f"🔍 DEBUG: Exclude regex {i}: {regex.pattern}")

        for pattern in patterns:
            logger.info(f"🔍 DEBUG: Processing pattern: {pattern}")

            if pattern.startswith("*."):
                # Extension pattern like *.py
                ext = pattern[2:]
                logger.info(f"🔍 DEBUG: Extension pattern - looking for *.{ext}")

                matches = list(root.rglob(f"*.{ext}"))
                logger.info(f"🔍 DEBUG: Found {len(matches)} raw matches for *.{ext}")

                filtered = []
                for f in matches:
                    if f.is_file():
                        # Check against exclude patterns - use search() not match()
                        file_str = str(f)
                        excluded = False

                        for regex in exclude_regexes:
                            if regex.search(file_str):
                                logger.info(
                                    f"🔍 DEBUG: EXCLUDED {file_str} by regex {regex.pattern}"
                                )
                                excluded = True
                                break

                        if not excluded:
                            # 🔧 SIMPLIFIED: No need to translate paths - they're already correct
                            filtered.append(file_str)
                            logger.info(f"🔍 DEBUG: INCLUDED {file_str}")

                logger.info(f"🔍 DEBUG: After filtering: {len(filtered)} files for *.{ext}")
                files_to_index.extend(filtered)
            else:
                # Full pattern like src/**/*.py
                logger.info(f"🔍 DEBUG: Full pattern - looking for {pattern}")

                matches = list(root.rglob(pattern))
                logger.info(f"🔍 DEBUG: Found {len(matches)} raw matches for {pattern}")

                filtered = []
                for f in matches:
                    if f.is_file():
                        # Check against exclude patterns
                        file_str = str(f)
                        excluded = False

                        for regex in exclude_regexes:
                            if regex.search(file_str):
                                logger.info(
                                    f"🔍 DEBUG: EXCLUDED {file_str} by regex {regex.pattern}"
                                )
                                excluded = True
                                break

                        if not excluded:
                            # 🔧 SIMPLIFIED: No need to translate paths - they're already correct
                            filtered.append(file_str)
                            logger.info(f"🔍 DEBUG: INCLUDED {file_str}")

                logger.info(f"🔍 DEBUG: After filtering: {len(filtered)} files for {pattern}")
                files_to_index.extend(filtered)

        # Remove duplicates
        files_to_index = list(set(files_to_index))

        logger.info(
            "🔍 DEBUG: File collection complete",
            total_files=len(files_to_index),
            patterns_count=len(patterns),
            first_10_files=files_to_index[:10] if files_to_index else "None",
        )

        return files_to_index

    except Exception as e:
        logger.error("Failed to collect files", error=str(e), exc_info=True)
        return []


async def _estimate_without_full_scan(root: Path, patterns: List[str]) -> int:
    """
    Estimate file count without doing a full scan.

    Uses heuristics and sampling to provide a quick approximation.
    This is only for user feedback, not for actual processing.
    """
    try:
        logger.info(f"Starting estimation for path: {root}")
        logger.info(f"Patterns to estimate: {patterns}")

        # Quick sampling approach - check a few directories
        sample_size = 0
        dirs_checked = 0
        max_dirs_to_check = 10

        # Common source directories to sample
        common_dirs = ["src", "lib", "app", "components", "pages", "api", "tests", "test"]
        dirs_to_check = []

        logger.info(f"Looking for common directories in {root}...")

        # Add common directories if they exist
        for dir_name in common_dirs:
            dir_path = root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                dirs_to_check.append(dir_path)
                logger.info(f"Found directory: {dir_name}")

        # If no common dirs found, sample from root
        if not dirs_to_check:
            logger.info("No common directories found, sampling from root...")
            # Get first few directories from root
            for item in root.iterdir():
                if (
                    item.is_dir()
                    and not item.name.startswith(".")
                    and item.name not in ["node_modules", "venv", ".git", "dist", "build"]
                ):
                    dirs_to_check.append(item)
                    logger.info(f"Added directory for sampling: {item.name}")
                    if len(dirs_to_check) >= max_dirs_to_check:
                        break

        logger.info(f"Total directories to sample: {len(dirs_to_check)}")

        # Sample files from selected directories
        for dir_path in dirs_to_check[:max_dirs_to_check]:
            try:
                logger.info(f"Sampling directory: {dir_path.name}...")
                files_in_dir = 0

                # Count files matching patterns in this directory (non-recursive)
                for file_path in dir_path.iterdir():
                    if file_path.is_file():
                        # Check if file matches any pattern
                        file_name = file_path.name
                        for pattern in patterns:
                            if pattern.startswith("*."):
                                ext = pattern[1:]  # Remove * to get .ext
                                if file_name.endswith(ext):
                                    sample_size += 1
                                    files_in_dir += 1
                                    break

                logger.info(f"Found {files_in_dir} matching files in {dir_path.name}")
                dirs_checked += 1
            except (PermissionError, OSError) as e:
                logger.warning(f"Error sampling directory {dir_path.name}: {e}")
                continue

        logger.info(f"Sampling complete. Dirs checked: {dirs_checked}, Files found: {sample_size}")

        # Extrapolate based on sample
        if dirs_checked > 0 and sample_size > 0:
            # Estimate total directories (rough approximation)
            total_dirs_estimate = max(20, dirs_checked * 5)  # Assume we sampled ~20% of dirs
            estimated_files = int(sample_size * (total_dirs_estimate / dirs_checked))

            # Apply reasonable bounds
            estimated_files = max(10, min(estimated_files, 10000))

            logger.info(
                "File estimation by sampling",
                sample_size=sample_size,
                dirs_checked=dirs_checked,
                estimated_total=estimated_files,
            )

            return estimated_files
        else:
            # No files found in sample, return conservative estimate
            logger.info("No files found in sample, returning conservative estimate of 100")
            return 100

    except Exception as e:
        logger.warning("Failed to estimate files by sampling", error=str(e))
        # Return conservative estimate
        return 100


async def _run_project_indexing(
    task_id: str, files_to_index: List[str], request: ProjectIndexRequest, estimated_files: int
) -> None:
    """
    Executes the project indexing in background.

    PROGRESS FLOW:
    1. IndexingService calls _notify_progress() internally
    2. _notify_progress() publishes ProgressEvent to the EventBus
    3. WebSocket handler listens to events where task_id appears in the message
    4. WebSocket sends updates to the client automatically

    No manual notification is required - the system is reactive via EventBus.
    """
    try:
        # 🔍 DEBUG: Show what files are being indexed
        logger.info("🔍 DEBUG: _run_project_indexing called")
        logger.info(f"🔍 DEBUG: task_id = {task_id}")
        logger.info(f"🔍 DEBUG: files_to_index count = {len(files_to_index)}")
        logger.info(f"🔍 DEBUG: estimated_files = {estimated_files}")
        logger.info(
            f"🔍 DEBUG: request.project_path = {getattr(request, 'project_path', 'NOT SET')}"
        )

        # Show first few files to index
        if files_to_index:
            logger.info("🔍 DEBUG: First 5 files to index:")
            for i, file_path in enumerate(files_to_index[:5]):
                logger.info(f"🔍 DEBUG: [{i+1}] {file_path}")
        else:
            logger.error("🔍 DEBUG: NO FILES TO INDEX!")

        logger.info("Starting project indexing", task_id=task_id, files_count=len(files_to_index))

        # Update progress tracker
        progress_tracker.update_task(
            task_id, message="Starting file indexing...", status=TaskStatus.RUNNING
        )

        # 🔧 SIMPLIFIED: Use request.project_path directly - it's already correct
        # No need to detect Docker again - index_project() already handled it
        indexing_service = IndexingService(project_path=request.project_path)

        logger.info(f"🔍 DEBUG: IndexingService created with project_path = {request.project_path}")

        # The progress is notified automatically when IndexingService processes files
        # The WebSocket will detect events with "Task: {task_id}" in the message

        # Index using the real service
        # IndexingService will include "Task: {task_id}" in the progress messages
        # so the WebSocket can filter events for this specific task
        await indexing_service.index_files(
            files=files_to_index,
            trigger="manual",
            task_id=task_id,  # Now pass the task_id for precise filtering
            resume_from=request.resume_task_id,  # Enable resuming from previous task
        )

        logger.info("Project indexing completed", task_id=task_id)

        # Mark task as completed in tracker
        progress_tracker.complete_task(task_id, "Indexing completed successfully")

    except Exception as e:
        logger.error("Project indexing failed", task_id=task_id, error=str(e), exc_info=True)
        progress_tracker.fail_task(task_id, f"Indexing failed: {str(e)}")
        # We could also publish an ErrorEvent to the EventBus for WebSocket notification
        # or we could publish an ErrorEvent to the EventBus (TODO)


async def _process_file_change(
    project_root: Path, file_change: GitChangeFile, trigger: str, commit_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Processes an individual file change.
    """
    try:
        # Validate path safely with pathlib
        try:
            # Use resolve() with strict=False to handle files that don't exist yet
            file_path = (project_root / file_change.path).resolve(strict=False)

            # Verify that the resolved path is inside the project
            try:
                file_path.relative_to(project_root)
            except ValueError:
                # The path is outside the project
                return {
                    "file": file_change.path,
                    "action": file_change.action,
                    "status": "skipped",
                    "reason": "outside_project",
                }

            # Verify against malicious symlinks
            if file_path.exists() and file_path.is_symlink():
                # Resolve the symlink and verify that it points inside the project
                real_path = file_path.resolve(strict=True)
                try:
                    real_path.relative_to(project_root)
                except ValueError:
                    logger.info("[TRACE] _process_file_change: symlink outside project")
                    return {
                        "file": file_change.path,
                        "action": file_change.action,
                        "status": "skipped",
                        "reason": "symlink_outside_project",
                    }

        except (ValueError, OSError) as e:
            logger.warning("Invalid path", path=file_change.path, error=str(e))
            return {
                "file": file_change.path,
                "action": file_change.action,
                "status": "skipped",
                "reason": "invalid_path",
                "error": str(e),
            }

        # Verify if the file should be indexed (using IndexingService logic)
        # 🔧 CRITICAL FIX: Pass project_root as project_path to IndexingService
        indexing_service = IndexingService(project_path=str(project_root))
        if not indexing_service.is_supported_file(file_path):
            return {
                "file": file_change.path,
                "action": file_change.action,
                "status": "skipped",
                "reason": "unsupported_file_type",
            }

        # Process according to the action
        if file_change.action == "deleted":
            # Remove from the index using IndexingService
            success = await indexing_service.remove_file(str(file_path))
            return {
                "file": file_change.path,
                "action": "removed",
                "status": "processed" if success else "error",
                "success": success,
            }

        elif file_change.action in ["added", "modified"]:
            # Re-index the file using IndexingService
            await indexing_service.index_files(
                files=[str(file_path)],
                trigger=trigger,
                task_id=None,  # Git hooks don't have a specific task_id
            )

            return {
                "file": file_change.path,
                "action": "indexed",
                "status": "processed",
                "chunks_created": 0,
                "embeddings_created": 0,
            }

        elif file_change.action == "renamed":
            # Update references in the index
            if file_change.old_path:
                success = await indexing_service.rename_file(
                    old_path=file_change.old_path, new_path=str(file_path)
                )
                return {
                    "file": file_change.path,
                    "action": "renamed",
                    "status": "processed" if success else "error",
                    "old_path": file_change.old_path,
                    "success": success,
                }
            else:
                return {
                    "file": file_change.path,
                    "action": "renamed",
                    "status": "error",
                    "error": "old_path required for rename operation",
                }

        return {
            "file": file_change.path,
            "action": file_change.action,
            "status": "skipped",
            "reason": "unknown_action",
        }

    except Exception as e:
        logger.error("Failed to process file change", path=file_change.path, error=str(e))
        return {
            "file": file_change.path,
            "action": file_change.action,
            "status": "error",
            "error": str(e),
        }
