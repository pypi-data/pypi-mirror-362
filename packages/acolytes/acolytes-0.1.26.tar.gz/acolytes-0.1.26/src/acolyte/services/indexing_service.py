"""
Indexing Service - Indexing Pipeline.

Orchestrates the complete code indexing pipeline.
"""

from acolyte.core.utils.datetime_utils import utc_now, utc_now_iso
from acolyte.core.utils.file_types import FileTypeDetector, FileCategory
from pathlib import Path
from typing import List, Dict, Any, Optional, TYPE_CHECKING, cast, Union
import re
import asyncio
import os
import time
import json
from charset_normalizer import detect
from dataclasses import dataclass, field
import threading

from acolyte.core.logging import logger, PerformanceLogger
from acolyte.core.tracing import MetricsCollector
from acolyte.core.exceptions import ExternalServiceError
from acolyte.core.secure_config import Settings
from acolyte.core.events import event_bus, ProgressEvent
from acolyte.models.chunk import Chunk, ChunkType
from acolyte.models.document import DocumentType
from acolyte.core.utils.retry import retry_async

# from acolyte.embeddings.types import EmbeddingVector  # Import only when needed

# Conditional imports while modules are being developed
try:
    from acolyte.rag.enrichment.service import EnrichmentService

    ENRICHMENT_AVAILABLE = True
except ImportError:
    logger.warning("EnrichmentService not available yet")
    ENRICHMENT_AVAILABLE = False

# Embeddings will be imported lazily when needed
EMBEDDINGS_AVAILABLE = None  # Will check on first use

# Weaviate will be imported when needed
WEAVIATE_AVAILABLE = True

if TYPE_CHECKING:
    from acolyte.embeddings.unixcoder import UniXcoderEmbeddings


@dataclass
class IndexingReport:
    total_files: int
    successful_files: int
    failed_files: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)

    def to_user_friendly_dict(self) -> Dict[str, Any]:
        return {
            'Total files': self.total_files,
            'Files indexed successfully': self.successful_files,
            'Failed files': len(self.failed_files),
            'Errors': self.failed_files,
            'Warnings': self.warnings,
            'Summary': self.summary,
        }


class IndexingService:
    """
    Orchestrates complete indexing pipeline.

    PIPELINE:
    1. Chunking → splits files
    2. Enrichment → adds Git metadata (returns tuples)
    3. Embeddings → vectorizes
    4. Weaviate → stores everything

    TRIGGERS:
    - "manual": User requested
    - "commit": Post-commit hook
    - "pull": Post-merge (invalidates cache)
    - "checkout": Branch change
    - "fetch": Preparation
    """

    def __init__(self, project_path: Optional[str] = None) -> None:
        self.metrics = MetricsCollector()
        self.perf_logger = PerformanceLogger()
        self.config = Settings()

        # Initialize available services
        if ENRICHMENT_AVAILABLE:
            # 🔧 CRITICAL FIX: Pass project_path to EnrichmentService to fix Git repository warning
            # This ensures EnrichmentService looks for Git repo in the correct project directory
            # instead of the Docker container's working directory
            self.enrichment = EnrichmentService(project_path or ".")
        else:
            self.enrichment = None

        # Embeddings will be loaded lazily
        self.embeddings: Optional["UniXcoderEmbeddings"] = None

        if WEAVIATE_AVAILABLE:
            self._init_weaviate()
        else:
            self.weaviate = None

        # Indexing configuration
        self.batch_size = self.config.get("indexing.batch_size", 20)
        self.large_dataset_batch_size = self.config.get("indexing.large_dataset_batch_size", 48)
        self.max_file_size_mb = self.config.get("indexing.max_file_size_mb", 10)
        self.concurrent_workers = self.config.get("indexing.concurrent_workers", 4)
        self.enable_parallel = self.config.get("indexing.enable_parallel", True)

        # Ignored files cache
        self._ignore_patterns = []
        self._load_ignore_patterns()

        # Failed files tracking
        self._failed_files = []

        # Lock to prevent concurrent indexing
        self._indexing_lock: asyncio.Lock = asyncio.Lock()
        self._is_indexing = False

        # Lock to prevent concurrent embeddings initialization
        self._embeddings_lock = threading.Lock()

        # Lazy-loaded worker pool for parallel processing
        self._worker_pool = None

        # Background cleanup tasks tracking
        self._cleanup_tasks: List["asyncio.Task[None]"] = []

        # ARCHITECTURAL DECISION (2025-07-04):
        # Progress checkpoints use job_states table directly instead of RuntimeStateManager.
        # Rationale:
        # - job_states provides structured fields (job_type, status, progress, total)
        # - Better queries with indexed fields for job monitoring
        # - RuntimeStateManager remains for simple key-value config (device fallbacks, etc)
        # Methods _save_progress, _load_progress, _clear_progress use job_states directly.

        # Checkpoint interval (save progress every N files)
        self.checkpoint_interval = self.config.get("indexing.checkpoint_interval", 50)

        # NOTE: Cache invalidation handling moved to ReindexService

        logger.info(
            "IndexingService initialized",
            enrichment=ENRICHMENT_AVAILABLE,
            embeddings="lazy",  # Will load on first use
            weaviate=WEAVIATE_AVAILABLE,
            parallel_enabled=self.enable_parallel,
            concurrent_workers=self.concurrent_workers if self.enable_parallel else "disabled",
        )

    def _ensure_embeddings(self):
        """Lazy load embeddings service when needed."""
        global EMBEDDINGS_AVAILABLE

        # Fast path: if already initialized, return immediately
        if self.embeddings is not None:
            return True

        # Thread-safe initialization
        with self._embeddings_lock:
            # Double-check pattern: another thread might have initialized while waiting
            if self.embeddings is not None:
                return True

            if EMBEDDINGS_AVAILABLE is None:
                try:
                    from acolyte.embeddings import get_embeddings

                    EMBEDDINGS_AVAILABLE = True
                    self.embeddings = get_embeddings()
                    logger.info("Embeddings service loaded on demand")
                except ImportError:
                    logger.warning("Embeddings service not available")
                    EMBEDDINGS_AVAILABLE = False

        return self.embeddings is not None

    def _init_weaviate(self):
        """Initialize Weaviate client."""
        try:
            import weaviate  # type: ignore

            # Obtener la URL de Weaviate respetando la variable de entorno
            weaviate_url = os.getenv(
                "WEAVIATE_URL", f"http://localhost:{self.config.get('ports.weaviate', 8080)}"
            )
            self.weaviate = weaviate.Client(weaviate_url)

            # Verify connection
            if not self.weaviate.is_ready():
                logger.warning("Weaviate not ready")
                self.weaviate = None

        except Exception as e:
            logger.error("Failed to connect to Weaviate", error=str(e))
            self.weaviate = None

    def _load_ignore_patterns(self):
        """Load patterns from .acolyteignore."""
        patterns_list = []
        ignore_config = self.config.get("ignore", {})

        def _extract_patterns(config_section):
            """Recursively extract patterns from nested configuration."""
            extracted = []
            for key, value in config_section.items():
                if isinstance(value, list):
                    # Direct list of patterns
                    extracted.extend(value)
                elif isinstance(value, dict):
                    # Nested dictionary - recurse
                    extracted.extend(_extract_patterns(value))
            return extracted

        patterns_list = _extract_patterns(ignore_config)
        self._ignore_patterns = [self._glob_to_regex(p) for p in patterns_list]
        logger.info("Loaded ignore patterns", patterns_count=len(self._ignore_patterns))

    def _glob_to_regex(self, pattern: str) -> re.Pattern:
        """Convert glob pattern to regex."""
        # Para directorios que terminan en /, coincidir con todo dentro
        if pattern.endswith("/"):
            # .git/ debe coincidir con .git/config, .git/hooks/pre-commit, etc.
            dir_name = pattern[:-1]  # Quitar el /
            # Escapar el nombre del directorio
            dir_name_escaped = re.escape(dir_name)
            # Pattern que coincida con:
            # - Al inicio: ^dir_name/anything
            # - En medio: /dir_name/anything
            # El .* al final asegura que coincida con cualquier archivo dentro del directorio
            regex_pattern = f"(^{dir_name_escaped}/.*|/{dir_name_escaped}/.*)"
            return re.compile(regex_pattern)

        # Para otros patterns, usar conversión mejorada
        # Escape special regex characters
        pattern = pattern.replace(".", r"\.")
        pattern = pattern.replace("**", "__DOUBLE_STAR__")  # Marcador temporal para **
        pattern = pattern.replace("*", "[^/]*")  # * no cruza directorios
        pattern = pattern.replace("__DOUBLE_STAR__", ".*")  # ** cruza directorios
        pattern = pattern.replace("?", ".")

        # Para archivos como *.pyc, hacerlos coincidir en cualquier directorio
        if pattern.startswith(r"[^/]*\."):
            pattern = "(^|.*/)" + pattern + "$"

        return re.compile(pattern)

    def _should_ignore(self, file_path: str) -> bool:
        """Check if a file should be ignored."""
        path_str = str(file_path)
        # Normalizar separadores para consistencia
        path_str = path_str.replace('\\', '/')

        for pattern in self._ignore_patterns or []:
            # Usar search() en lugar de match() para buscar en cualquier parte
            if pattern.search(path_str):
                return True

        return False

    async def _cleanup_indexing_resources(self) -> None:
        """Clean up resources that might be left from previous indexing operations.

        This includes:
        - Closing any hanging database connections
        - Clearing temporary caches
        - Resetting worker pools if needed
        """
        try:
            # Clean up worker pool if exists AND not currently indexing
            if (
                hasattr(self, '_worker_pool')
                and self._worker_pool is not None
                and not self._is_indexing
            ):
                try:
                    # Worker pool cleanup (use shutdown method instead of cleanup)
                    if hasattr(self._worker_pool, 'shutdown'):
                        await self._worker_pool.shutdown()
                    self._worker_pool = None
                    logger.debug("Worker pool cleaned up during non-indexing state")
                except asyncio.CancelledError:
                    logger.debug("Worker pool cleanup was cancelled - normal during shutdown")
                    self._worker_pool = None  # Still clear the reference
                except Exception as e:
                    logger.warning(
                        "Error cleaning worker pool", error=str(e), error_type=type(e).__name__
                    )
                    self._worker_pool = None  # Clear reference even on error
            elif self._is_indexing:
                logger.debug("Skipping worker pool cleanup - indexing in progress")

            # Clean up any hanging Weaviate batch operations
            if hasattr(self, 'batch_inserter') and self.batch_inserter is not None:
                try:
                    # Batch inserter cleanup (just clear the reference)
                    delattr(self, 'batch_inserter')
                except Exception as e:
                    logger.warning("Error cleaning batch inserter", error=str(e))

            # Clear any cached failed files
            if hasattr(self, '_failed_files'):
                self._failed_files = []

        except Exception as e:
            logger.error("Failed to clean indexing resources", error=str(e))
            # Don't raise - this is a best-effort cleanup

    async def index_files(
        self,
        files: List[str],
        trigger: str = "manual",
        task_id: Optional[str] = None,
        resume_from: Optional[str] = None,
    ) -> Dict[str, Any]:
        # ✅ OPTIMIZED: SQLite artifacts cleanup handled automatically by DatabaseManager
        # No need for manual cleanup - DatabaseManager._cleanup_sqlite_artifacts() handles this

        # 🔧 REMOVED: Aggressive database closing that caused Windows fatal exceptions
        # The aggressive close() calls were causing race conditions with concurrent database operations
        # DatabaseManager handles connection management automatically and safely

        # Limpiar checkpoints viejos antes de empezar
        await self._clear_old_checkpoints(days=7)

        # CRÍTICO: Cleanup automático de estado corrupto (interrupciones)
        # Esto NO afecta checkpoints ni la base de datos, solo limpia memoria/conexiones
        await self._cleanup_corrupted_state()

        # 🔧 CRITICAL FIX: Cleanup resources left from previous indexing
        # Esto previene deadlocks causados por recursos no cerrados anteriormente
        # FIXED: Wait for cleanup to complete BEFORE starting indexing to prevent race condition
        try:
            await self._cleanup_indexing_resources()
            logger.debug("Pre-indexing cleanup completed successfully")
        except Exception as e:
            logger.warning("Error cleaning previous indexing resources", error=str(e))

        # Atomic check-and-set to prevent race condition
        async with self._indexing_lock:
            if self._is_indexing:
                raise Exception("Indexing already in progress")
            self._is_indexing = True

        try:
            start_time = utc_now()

            # Validate trigger
            VALID_TRIGGERS = {"commit", "pull", "checkout", "fetch", "manual"}
            if trigger not in VALID_TRIGGERS:
                logger.warning("Unknown indexing trigger", trigger=trigger, fallback="manual")
                trigger = "manual"

            logger.info("Starting indexing", files_count=len(files), trigger=trigger)

            # Check for resumable progress
            if resume_from:
                progress = await self._load_progress(resume_from)
                if progress and progress.get("status") == "in_progress":
                    # Resume from saved progress
                    files_pending = progress.get("files_pending", [])
                    if files_pending:
                        logger.info(
                            "Resuming indexing from checkpoint",
                            task_id=resume_from,
                            total_files=progress.get("total_files", 0),
                            processed_files=progress.get("processed_files", 0),
                            pending_files=len(files_pending),
                        )
                        files = files_pending
                        # Restore counters
                        total_chunks = progress.get("chunks_created", 0)
                        total_embeddings = progress.get("embeddings_created", 0)
                        errors = progress.get("errors", [])
                        files_skipped = progress.get("files_skipped", 0)
                        resumed = True
                    else:
                        logger.warning("No pending files in saved progress", task_id=resume_from)
                        resumed = False
                else:
                    logger.info("No resumable progress found", task_id=resume_from)
                    resumed = False
            else:
                resumed = False

            # Filter files if not resuming
            if not resumed:
                with self.perf_logger.measure("indexing_filter_files", files_count=len(files)):
                    valid_files = await self._filter_files(files)
                files_skipped = len(files) - len(valid_files)  # Calculate skipped files
                total_chunks = 0
                total_embeddings = 0
                errors = []
            else:
                # When resuming, files are already filtered
                valid_files = files

            if not valid_files:
                return {
                    "status": "success",
                    "files_requested": len(files),
                    "files_processed": 0,
                    "reason": "All files filtered out",
                    "trigger": trigger,
                    "chunks_created": 0,
                    "embeddings_created": 0,
                    "duration_seconds": 0,
                    "errors": [],
                }

            # Decide whether to use parallel processing
            # ALWAYS use parallel processing when enabled for maximum performance
            use_parallel = self.enable_parallel and self.concurrent_workers > 1

            # BATCH MODE: For very large datasets (>200 files), use automatic batching for memory management
            if len(valid_files) > 200 and self.enable_parallel:
                logger.info(
                    "Very large dataset detected, using batch mode for memory management",
                    total_files=len(valid_files),
                    batch_size=self.large_dataset_batch_size,
                )
                batch_result = await self._index_files_in_batches(
                    valid_files,
                    batch_size=self.large_dataset_batch_size,
                    trigger=trigger,
                    task_id=task_id,
                )
                return batch_result

            if use_parallel:
                # Use worker pool for parallel processing
                logger.info(
                    "Using parallel processing",
                    workers=self.concurrent_workers,
                    files=len(valid_files),
                )

                # Initialize worker pool if needed
                if self._worker_pool is None:
                    from acolyte.services.indexing_worker_pool import IndexingWorkerPool

                    embeddings_semaphore = self.config.get("indexing.embeddings_semaphore", 2)
                    self._worker_pool = IndexingWorkerPool(
                        indexing_service=self,
                        num_workers=self.concurrent_workers,
                        embeddings_semaphore_size=embeddings_semaphore,
                    )
                    await self._worker_pool.initialize()

                # Process files in parallel
                worker_batch_size = self.config.get("indexing.worker_batch_size", 12)
                pool_result = await self._worker_pool.process_files(
                    valid_files, batch_size=worker_batch_size, trigger=trigger
                )

                # Extract results
                total_chunks = pool_result["chunks_created"]
                total_embeddings = pool_result["embeddings_created"]
                errors = pool_result["errors"]

                # Notify final progress
                await self._notify_progress(
                    {
                        "total_files": len(valid_files),
                        "processed_files": len(valid_files),
                        "current_file": "Complete",
                        "percentage": 100,
                    },
                    task_id=task_id,
                    files_skipped=files_skipped,
                    chunks_created=total_chunks,
                    embeddings_generated=total_embeddings,
                    errors_count=len(errors),
                )

                # Process finished
                end_time = utc_now()
                duration = (end_time - start_time).total_seconds()

                result = {
                    "status": "success",
                    "files_requested": len(files),
                    "files_processed": len(valid_files),
                    "files_skipped": files_skipped,
                    "chunks_created": total_chunks,
                    "embeddings_created": total_embeddings,
                    "duration_seconds": round(duration, 2),
                    "errors": errors,
                    "trigger": trigger,
                    "parallel_workers": self.concurrent_workers,
                    "mode": "parallel",
                }

                # Clear progress if completed successfully
                if task_id and result["status"] in ["success", "partial"]:
                    await self._clear_progress(task_id)
                    logger.debug("Indexing progress cleared", task_id=task_id)

                return result

            else:
                # Use sequential processing as fallback (parallel disabled or only 1 worker)
                logger.info(
                    "Using sequential processing",
                    files=len(valid_files),
                    reason="parallel_disabled",
                )
                total_chunks = 0
                total_embeddings = 0
                errors = []

                for i, file in enumerate(valid_files):
                    try:
                        # Notify progress
                        await self._notify_progress(
                            {
                                "total_files": len(valid_files),
                                "processed_files": i,
                                "current_file": file,
                                "percentage": int((i / len(valid_files)) * 100),
                            },
                            task_id=task_id,
                            files_skipped=files_skipped,
                            chunks_created=total_chunks,
                            embeddings_generated=total_embeddings,
                            errors_count=len(errors),
                        )

                        # Process batch with single file
                        batch_result = await self._process_batch([file], trigger)
                        total_chunks += batch_result["chunks_created"]
                        total_embeddings += batch_result["embeddings_created"]
                        errors.extend(batch_result["errors"])

                        # Save progress checkpoint
                        if (i + 1) % self.checkpoint_interval == 0:
                            await self._save_progress(
                                task_id or "no_task",
                                {
                                    "task_id": task_id or "no_task",
                                    "status": "in_progress",
                                    "total_files": len(valid_files),
                                    "processed_files": i + 1,
                                    "files_pending": valid_files[i + 1 :],
                                    "chunks_created": total_chunks,
                                    "embeddings_created": total_embeddings,
                                    "errors": errors,
                                    "files_skipped": files_skipped,
                                },
                            )

                    except Exception as e:
                        logger.error(
                            "Error processing file in sequential mode",
                            file=file,
                            error=str(e),
                            error_type=type(e).__name__,
                        )
                        errors.append(
                            {
                                "file": file,
                                "error": str(e),
                                "error_type": type(e).__name__,
                            }
                        )

                # Final progress notification
                await self._notify_progress(
                    {
                        "total_files": len(valid_files),
                        "processed_files": len(valid_files),
                        "current_file": "Complete",
                        "percentage": 100,
                    },
                    task_id=task_id,
                    files_skipped=files_skipped,
                    chunks_created=total_chunks,
                    embeddings_generated=total_embeddings,
                    errors_count=len(errors),
                )

                # Process finished
                end_time = utc_now()
                duration = (end_time - start_time).total_seconds()

                result = {
                    "status": "success",
                    "files_requested": len(files),
                    "files_processed": len(valid_files),
                    "files_skipped": files_skipped,
                    "chunks_created": total_chunks,
                    "embeddings_created": total_embeddings,
                    "duration_seconds": round(duration, 2),
                    "errors": errors,
                    "trigger": trigger,
                    "mode": "sequential",
                }

            # Clear progress if completed successfully
            if task_id and result["status"] in ["success", "partial"]:
                await self._clear_progress(task_id)
                logger.debug("Indexing progress cleared", task_id=task_id)

            return result
        finally:
            # 🔧 CRITICAL FIX: Cleanup resources created during indexing
            # This prevents hanging resources that can affect future indexing
            try:
                # Start cleanup in background and track the task
                cleanup_task = asyncio.create_task(self._cleanup_indexing_resources())
                self._cleanup_tasks.append(cleanup_task)

                # Add robust error handler for cleanup task
                def cleanup_callback(task):
                    if task.cancelled():
                        logger.debug(
                            "Cleanup task was cancelled - this is expected during shutdown"
                        )
                        return

                    exc = task.exception()
                    if exc is not None:
                        if isinstance(exc, asyncio.CancelledError):
                            logger.debug(
                                "Cleanup task received CancelledError - normal during shutdown"
                            )
                        else:
                            logger.error(
                                "Cleanup task failed", error=str(exc), error_type=type(exc).__name__
                            )
                    else:
                        logger.debug("Cleanup task completed successfully")

                cleanup_task.add_done_callback(cleanup_callback)
            except Exception as e:
                logger.warning("Error during resource cleanup", error=str(e))

            # 🔧 REMOVED: Aggressive database closing that caused Windows fatal exceptions
            # The aggressive close() calls were causing race conditions with concurrent database operations
            # DatabaseManager handles connection management automatically and safely

            # ✅ OPTIMIZED: SQLite artifacts cleanup handled automatically by DatabaseManager
            # No need for manual cleanup - DatabaseManager._cleanup_sqlite_artifacts() handles this

            # Use lock to safely clear the flag
            async with self._indexing_lock:
                self._is_indexing = False

    async def _filter_files(self, files: List[str]) -> List[str]:
        """Filter valid files to index."""
        valid_files = []

        for file_path in files:
            path = Path(file_path).resolve()

            # Verify it exists
            if not path.exists():
                logger.debug("File not found", file_path=file_path)
                continue

            # Verify it's not a directory
            if path.is_dir():
                continue

            # Verify size
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > self.max_file_size_mb:
                logger.warning(
                    "File too large for indexing",
                    file=file_path,
                    size_mb=round(size_mb, 1),
                    limit_mb=self.max_file_size_mb,
                )
                continue

            # Verify ignore patterns
            if self._should_ignore(str(path)):
                logger.debug("File ignored by patterns", file_path=file_path)
                continue

            # Verify supported extension
            if not self._is_supported_file(path):
                logger.debug("Unsupported file type", file_path=file_path)
                continue

            valid_files.append(str(path))

        return valid_files

    def _is_supported_file(self, path: Path) -> bool:
        """Check if the file is of a supported type."""
        return FileTypeDetector.is_supported(path)

    async def _index_files_in_batches(
        self, files: List[str], batch_size: int, trigger: str, task_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process files in batches to prevent deadlock with large datasets.

        PHASE 2 IMPLEMENTATION: Advanced progress tracking with granular batch updates.
        - Real-time progress via EventBus per batch
        - Time estimation based on completed batches
        - Checkpoint saving after each batch
        - WebSocket updates for live UI feedback
        """
        total_files = len(files)
        batches = [files[i : i + batch_size] for i in range(0, total_files, batch_size)]
        total_batches = len(batches)

        # Phase 2: Start time tracking for accurate estimates
        batch_start_time = time.time()
        batch_times = []  # Track time per batch for estimation

        logger.info(
            "Starting batch processing with advanced progress tracking",
            total_files=total_files,
            total_batches=total_batches,
            batch_size=batch_size,
            trigger=trigger,
            task_id=task_id,
        )

        # Accumulated results
        total_results = {
            "status": "success",
            "files_requested": total_files,
            "files_processed": 0,
            "chunks_created": 0,
            "embeddings_created": 0,
            "errors": [],
            "trigger": trigger,
            "batch_info": {
                "total_batches": total_batches,
                "batch_size": batch_size,
                "completed_batches": 0,
            },
        }

        # Process each batch with advanced progress tracking
        for batch_idx, batch_files in enumerate(batches):
            batch_num = batch_idx + 1
            current_batch_start = time.time()

            # Phase 2: Calculate detailed progress information
            files_processed_so_far = sum(len(batches[i]) for i in range(batch_idx))

            # 🔧 FASE 3: Verificar si se solicitó pausa antes del batch
            if task_id and self._is_batch_paused(task_id):
                logger.info(
                    "Batch processing paused by user request",
                    batch_number=batch_num,
                    total_batches=total_batches,
                    task_id=task_id,
                )
                # Actualizar progress tracker
                self._update_progress_tracker(
                    task_id,
                    files_processed_so_far,
                    total_files,
                    f"Paused at batch {batch_num}",
                    {"paused_at_batch": batch_num, "total_batches": total_batches},
                )
                # Esperar hasta que se reanude
                while self._is_batch_paused(task_id):
                    await asyncio.sleep(1)
                logger.info("Batch processing resumed", task_id=task_id)
            progress_percentage = round((batch_idx / total_batches) * 100, 1)

            # Phase 2: Estimate remaining time based on completed batches
            estimated_remaining_seconds = 0
            if batch_times:
                avg_batch_time = sum(batch_times) / len(batch_times)
                remaining_batches = total_batches - batch_idx
                estimated_remaining_seconds = avg_batch_time * remaining_batches

            logger.info(
                "Processing batch with progress tracking",
                batch_number=batch_num,
                total_batches=total_batches,
                files_in_batch=len(batch_files),
                progress_percentage=progress_percentage,
                files_processed_so_far=files_processed_so_far,
                estimated_remaining_minutes=(
                    round(estimated_remaining_seconds / 60, 1)
                    if estimated_remaining_seconds > 0
                    else "calculating..."
                ),
            )

            # 🔧 FASE 3: Actualizar progress tracker al inicio del batch
            if task_id:
                self._update_progress_tracker(
                    task_id,
                    files_processed_so_far,
                    total_files,
                    f"Processing batch {batch_num}/{total_batches}",
                    {
                        "current_batch": batch_num,
                        "total_batches": total_batches,
                        "batch_status": "processing",
                        "estimated_remaining_seconds": estimated_remaining_seconds,
                    },
                )

            try:
                # Process this batch using PARALLEL processing with 4 workers
                # Each worker has separate EnrichmentService (deadlock already fixed)
                # Initialize worker pool if needed
                if self._worker_pool is None:
                    from acolyte.services.indexing_worker_pool import IndexingWorkerPool

                    embeddings_semaphore = self.config.get("indexing.embeddings_semaphore", 2)
                    self._worker_pool = IndexingWorkerPool(
                        indexing_service=self,
                        num_workers=self.concurrent_workers,
                        embeddings_semaphore_size=embeddings_semaphore,
                    )
                    await self._worker_pool.initialize()

                # Process batch files in parallel with 4 workers
                worker_batch_size = self.config.get("indexing.worker_batch_size", 12)

                # 🔧 CRITICAL FIX: Report progress during batch processing
                # Split batch into smaller chunks for more frequent progress updates
                mini_batch_size = max(
                    1, min(worker_batch_size, 5)
                )  # Process 5 files at a time for progress
                batch_result = {"chunks_created": 0, "embeddings_created": 0, "errors": []}

                for mini_batch_idx in range(0, len(batch_files), mini_batch_size):
                    mini_batch = batch_files[mini_batch_idx : mini_batch_idx + mini_batch_size]

                    # Process mini-batch
                    mini_result = await self._worker_pool.process_files(
                        mini_batch, batch_size=worker_batch_size, trigger=trigger
                    )

                    # Accumulate results
                    batch_result["chunks_created"] += mini_result.get("chunks_created", 0)
                    batch_result["embeddings_created"] += mini_result.get("embeddings_created", 0)
                    batch_result["errors"].extend(mini_result.get("errors", []))

                    # 🔧 CRITICAL FIX: Report progress after each mini-batch
                    files_processed_in_batch = mini_batch_idx + len(mini_batch)
                    total_files_processed_so_far = files_processed_so_far + files_processed_in_batch

                    if task_id:
                        await self._notify_progress(
                            {
                                "total_files": total_files,
                                "processed_files": total_files_processed_so_far,
                                "current_file": f"Processing batch {batch_num}/{total_batches} - {files_processed_in_batch}/{len(batch_files)} files",
                                "percentage": round(
                                    (total_files_processed_so_far / total_files) * 100, 1
                                ),
                            },
                            task_id=task_id,
                            chunks_created=total_results["chunks_created"]
                            + batch_result["chunks_created"],
                            embeddings_generated=total_results["embeddings_created"]
                            + batch_result["embeddings_created"],
                            errors_count=len(total_results["errors"]) + len(batch_result["errors"]),
                            batch_num=batch_num,
                            total_batches=total_batches,
                            files_in_batch=files_processed_in_batch,
                            batch_status="processing",
                            estimated_remaining_seconds=estimated_remaining_seconds,
                        )

                # Accumulate results (worker_pool.process_files format)
                total_results["files_processed"] += len(batch_files)  # Files in current batch
                total_results["chunks_created"] += batch_result.get("chunks_created", 0)
                total_results["embeddings_created"] += batch_result.get("embeddings_created", 0)
                total_results["errors"].extend(batch_result.get("errors", []))
                total_results["batch_info"]["completed_batches"] = batch_num

                # Phase 2: Track batch completion time for estimates
                batch_elapsed = time.time() - current_batch_start
                batch_times.append(batch_elapsed)

                # Phase 2: Calculate updated progress after batch completion
                files_processed_after_batch = total_results["files_processed"]
                progress_percentage_completed = round(
                    (files_processed_after_batch / total_files) * 100, 1
                )

                # Log batch completion with enhanced metrics
                logger.info(
                    "Batch completed successfully with enhanced tracking",
                    batch_number=batch_num,
                    batch_duration_seconds=round(batch_elapsed, 1),
                    chunks_created=batch_result.get("chunks_created", 0),
                    embeddings_created=batch_result.get("embeddings_created", 0),
                    errors_in_batch=len(batch_result.get("errors", [])),
                    total_progress_percentage=progress_percentage_completed,
                    files_processed_total=files_processed_after_batch,
                )

                # Phase 2: Notify progress via EventBus after batch completion
                if task_id:
                    await self._notify_progress(
                        {
                            "total_files": total_files,
                            "processed_files": files_processed_after_batch,
                            "current_file": f"Batch {batch_num}/{total_batches} completed",
                            "percentage": progress_percentage_completed,
                        },
                        task_id=task_id,
                        chunks_created=total_results["chunks_created"],
                        embeddings_generated=total_results["embeddings_created"],
                        errors_count=len(total_results["errors"]),
                        # Phase 2: Add batch-specific information for completion
                        batch_num=batch_num,
                        total_batches=total_batches,
                        files_in_batch=len(batch_files),
                        batch_status="completed",
                        estimated_remaining_seconds=(
                            estimated_remaining_seconds if batch_num < total_batches else 0
                        ),
                    )

                # Phase 2: Save checkpoint after each batch completion
                if task_id:
                    # Calculate remaining files for resumability
                    remaining_batches = batches[batch_idx + 1 :]
                    remaining_files = [file for batch in remaining_batches for file in batch]

                    checkpoint_data = {
                        "task_id": task_id,
                        "status": "in_progress",
                        "started_at": utc_now_iso(),  # Will be overridden with actual start time
                        "total_files": total_files,
                        "processed_files": files_processed_after_batch,
                        "files_pending": remaining_files,
                        "files_skipped": 0,  # Will be calculated properly later
                        "chunks_created": total_results["chunks_created"],
                        "embeddings_created": total_results["embeddings_created"],
                        "errors": total_results["errors"],
                        "last_checkpoint": utc_now_iso(),
                        "trigger": trigger,
                        "batch_mode": True,
                        "batches_completed": batch_num,
                        "total_batches": total_batches,
                        "avg_batch_time_seconds": round(sum(batch_times) / len(batch_times), 2),
                        "estimated_remaining_seconds": (
                            round(estimated_remaining_seconds, 1)
                            if estimated_remaining_seconds > 0
                            else 0
                        ),
                    }

                    try:
                        await self._save_progress(task_id, checkpoint_data)
                        logger.debug(
                            "Batch checkpoint saved",
                            task_id=task_id,
                            batch_completed=batch_num,
                            total_batches=total_batches,
                            files_processed=files_processed_after_batch,
                        )
                    except Exception as e:
                        logger.warning(
                            "Failed to save batch checkpoint", task_id=task_id, error=str(e)
                        )

            except Exception as e:
                logger.error(
                    "Batch processing failed",
                    batch_number=batch_num,
                    error=str(e),
                    files_in_batch=len(batch_files),
                )

                # Add batch error to results
                batch_error = {
                    "batch": batch_num,
                    "error": str(e),
                    "files_affected": len(batch_files),
                    "error_type": type(e).__name__,
                }
                total_results["errors"].append(batch_error)

                # For Phase 1, continue processing remaining batches
                # User can configure this behavior in Phase 3
                continue

        # Calculate final statistics
        if total_results["errors"]:
            total_results["status"] = "partial"

        # Phase 2: Enhanced summary logging with performance metrics
        total_batch_time = time.time() - batch_start_time
        avg_batch_time = sum(batch_times) / len(batch_times) if batch_times else 0

        logger.info(
            "Batch processing completed with enhanced tracking",
            total_files=total_files,
            files_processed=total_results["files_processed"],
            chunks_created=total_results["chunks_created"],
            embeddings_created=total_results["embeddings_created"],
            total_errors=len(total_results["errors"]),
            completed_batches=total_results["batch_info"]["completed_batches"],
            status=total_results["status"],
            # Phase 2: Performance metrics
            total_time_seconds=round(total_batch_time, 1),
            avg_batch_time_seconds=round(avg_batch_time, 1),
            files_per_second=(
                round(total_files / total_batch_time, 2) if total_batch_time > 0 else 0
            ),
            batches_per_hour=round(3600 / avg_batch_time, 1) if avg_batch_time > 0 else 0,
        )

        # Phase 2: Final progress notification with completion
        if task_id:
            await self._notify_progress(
                {
                    "total_files": total_files,
                    "processed_files": total_results["files_processed"],
                    "current_file": "All batches completed",
                    "percentage": 100.0,
                },
                task_id=task_id,
                chunks_created=total_results["chunks_created"],
                embeddings_generated=total_results["embeddings_created"],
                errors_count=len(total_results["errors"]),
                batch_num=total_batches,
                total_batches=total_batches,
                files_in_batch=0,
                batch_status="all_completed",
                estimated_remaining_seconds=0,
            )

        return total_results

    async def _process_batch(self, files: List[str], trigger: str) -> Dict[str, Any]:
        """Process a batch of files."""
        chunks_created = 0
        embeddings_created = 0
        batch_errors = []
        # STEP 1: Chunking
        with self.perf_logger.measure("indexing_chunking", files_count=len(files)):
            chunks = await self._chunk_files(files)
            # Añadir errores de chunking
            if hasattr(self, '_failed_files') and self._failed_files:
                batch_errors.extend(self._failed_files)

        if not chunks:
            return {"chunks_created": 0, "embeddings_created": 0}

        # STEP 2: Enrichment - RETURNS TUPLES
        enriched_tuples = []
        with self.perf_logger.measure("indexing_enrichment", chunks_count=len(chunks)):
            if self.enrichment and ENRICHMENT_AVAILABLE:
                try:
                    enriched_tuples = await self.enrichment.enrich_chunks(
                        chunks, trigger=trigger  # EnrichmentService uses this for cache
                    )
                except Exception as e:
                    logger.error(
                        "Enrichment failed", chunks_count=len(chunks), trigger=trigger, error=str(e)
                    )
                    # Continue without enrichment
                    enriched_tuples = [(chunk, {}) for chunk in chunks]
            else:
                # Without enrichment, create empty tuples
                enriched_tuples = [(chunk, {}) for chunk in chunks]

        # STEP 3: Generate embeddings in batch (MUCH more efficient)
        from typing import Optional
        from acolyte.embeddings.types import EmbeddingVector
        from acolyte.core.exceptions import ExternalServiceError

        embeddings_list: list[Optional[EmbeddingVector]] = []
        if self._ensure_embeddings() and self.embeddings is not None:
            # Extract all chunk contents for batch processing
            chunks_content = [chunk.content for chunk, _ in enriched_tuples]

            if chunks_content:
                try:
                    with self.perf_logger.measure(
                        "indexing_batch_embedding_generation", chunks_count=len(chunks_content)
                    ):
                        max_tokens = self.config.get("embeddings.max_tokens_per_batch", 10000)
                        embeddings_service = self.embeddings  # Copia local para tipado

                        async def encode_batch_retry():
                            loop = asyncio.get_running_loop()
                            return await retry_async(
                                lambda: loop.run_in_executor(
                                    None,
                                    lambda: cast(
                                        list[Optional[EmbeddingVector]],
                                        embeddings_service.encode_batch(
                                            texts=cast(list[Union[str, Chunk]], chunks_content),
                                            max_tokens_per_batch=max_tokens,
                                        ),
                                    ),
                                ),
                                max_attempts=4,
                                retry_on=(ExternalServiceError, TimeoutError),
                                logger=logger,
                            )

                        embeddings_list = await encode_batch_retry()
                    embeddings_created = len(embeddings_list)
                    logger.info(
                        "Batch embedding generation successful",
                        chunks_count=len(chunks_content),
                        embeddings_created=embeddings_created,
                    )
                except Exception as e:
                    logger.error(
                        "Batch embedding generation failed, falling back to individual",
                        error=str(e),
                        chunks_count=len(chunks_content),
                    )
                    # Fallback: process one by one if batch fails
                    embeddings_service = self.embeddings  # Copia local para tipado
                    for chunk_content in chunks_content:
                        try:

                            async def encode_single():
                                loop = asyncio.get_running_loop()
                                return await loop.run_in_executor(
                                    None, lambda: embeddings_service.encode(chunk_content)
                                )

                            embedding = await retry_async(
                                encode_single,
                                max_attempts=3,
                                retry_on=(ExternalServiceError, TimeoutError),
                                logger=logger,
                            )
                            embeddings_list.append(embedding)
                            embeddings_created += 1
                        except Exception as individual_error:
                            logger.error("Individual embedding failed", error=str(individual_error))
                            embeddings_list.append(None)  # Placeholder for failed

        # STEP 4: Prepare for batch insertion
        if self.weaviate and WEAVIATE_AVAILABLE:
            # Check if batch insertion is enabled
            use_batch = self.config.get("search.weaviate_batch_size", 100) > 1

            if use_batch:
                # Prepare data for batch insertion
                weaviate_objects = []
                vectors_list = []

                for i, (chunk, enrichment_metadata) in enumerate(enriched_tuples):
                    # Combine all info for Weaviate
                    weaviate_object = self._prepare_weaviate_object(chunk, enrichment_metadata)
                    weaviate_objects.append(weaviate_object)

                    # Get corresponding embedding (if any)
                    embedding = embeddings_list[i] if i < len(embeddings_list) else None

                    if embedding:
                        # Import EmbeddingVector only when needed
                        from acolyte.embeddings.types import EmbeddingVector

                        # Validate embedding type
                        if isinstance(embedding, EmbeddingVector):
                            vector = embedding.to_weaviate()
                        elif hasattr(embedding, "to_weaviate"):
                            vector = embedding.to_weaviate()
                        else:
                            # Assume it's a list or array
                            vector = list(embedding)
                        vectors_list.append(vector)
                    else:
                        vectors_list.append(None)

                # Use batch inserter
                try:
                    with self.perf_logger.measure(
                        "indexing_weaviate_batch_insert", chunks_count=len(weaviate_objects)
                    ):
                        if not hasattr(self, "batch_inserter"):
                            from acolyte.rag.collections import WeaviateBatchInserter

                            self.batch_inserter = WeaviateBatchInserter(self.weaviate, self.config)

                        async def batch_insert_retry():
                            return await retry_async(
                                lambda: self.batch_inserter.batch_insert(
                                    data_objects=weaviate_objects,
                                    vectors=vectors_list,
                                    class_name="CodeChunk",
                                ),
                                max_attempts=4,
                                retry_on=(ExternalServiceError, TimeoutError),
                                logger=logger,
                            )

                        successful, errors = await batch_insert_retry()
                        chunks_created = successful
                        batch_errors.extend(errors)
                        logger.info(
                            "Batch insertion completed",
                            successful=successful,
                            failed=len(errors),
                            batch_size=len(weaviate_objects),
                        )
                except Exception as e:
                    logger.error(
                        "Batch insertion failed completely",
                        error=str(e),
                        chunks_count=len(weaviate_objects),
                    )
                    for chunk, _ in enriched_tuples:
                        file_path = getattr(chunk.metadata, "file_path", "unknown")
                        chunk_type = getattr(chunk.metadata, "chunk_type", "unknown")
                        error_detail = {
                            "file": file_path,
                            "chunk_type": chunk_type,
                            "error": "Batch insertion failed",
                            "error_type": "BatchInsertionError",
                        }
                        batch_errors.append(error_detail)
            else:
                # Fallback to individual insertion (original code)
                for i, (chunk, enrichment_metadata) in enumerate(enriched_tuples):
                    try:
                        embedding = embeddings_list[i] if i < len(embeddings_list) else None
                        weaviate_object = self._prepare_weaviate_object(chunk, enrichment_metadata)
                        with self.perf_logger.measure("indexing_weaviate_insert"):
                            await retry_async(
                                lambda: self._index_to_weaviate(weaviate_object, embedding),
                                max_attempts=4,
                                retry_on=(ExternalServiceError, TimeoutError),
                                logger=logger,
                            )
                        chunks_created += 1
                    except Exception as e:
                        file_path = getattr(chunk.metadata, "file_path", "unknown")
                        chunk_type = getattr(chunk.metadata, "chunk_type", "unknown")
                        error_detail = {
                            "file": file_path,
                            "chunk_type": chunk_type,
                            "error": str(e),
                            "error_type": type(e).__name__,
                        }
                        batch_errors.append(error_detail)
                        logger.error(
                            "Failed to process chunk",
                            file_path=file_path,
                            chunk_type=chunk_type,
                            error=str(e),
                            error_type=type(e).__name__,
                        )
                        continue

        return {
            "chunks_created": chunks_created,
            "embeddings_created": embeddings_created,
            "errors": batch_errors,
        }

    async def _chunk_files(self, files: List[str]) -> List[Chunk]:
        """
        Divide files into chunks with intelligent ChunkType detection.
        Fallback a DefaultChunker por archivo si AdaptiveChunker falla.
        Acumula archivos problemáticos en self._failed_files.
        """
        chunks = []
        self._failed_files = []

        # Import ChunkerFactory for per-file chunker creation
        from acolyte.rag.chunking.factory import ChunkerFactory

        for file_path in files:
            path = Path(file_path)
            try:
                try:
                    content = path.read_text(encoding="utf-8", errors="strict")
                except UnicodeDecodeError:
                    # Try charset detection first
                    encoding_detected = None
                    try:
                        with open(path, 'rb') as f:
                            raw = f.read(10000)  # Lee solo primeros 10KB para detectar
                            result = detect(raw)
                        if result and result.get('encoding'):
                            encoding_detected = result['encoding']
                            confidence = result.get('confidence', 0) or 0
                            if confidence > 0.7:
                                logger.debug(
                                    "Detected encoding with confidence",
                                    encoding=encoding_detected,
                                    confidence=confidence,
                                )
                    except Exception as e:
                        logger.debug(
                            "Charset detection failed for file", file_path=file_path, error=str(e)
                        )
                    # Try detected encoding or fallback to common encodings
                    encodings_to_try = []
                    if encoding_detected:
                        encodings_to_try.append(encoding_detected)
                    # Add common fallback encodings
                    encodings_to_try.extend(
                        ['utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
                    )
                    content = None
                    for encoding in encodings_to_try:
                        try:
                            content = path.read_text(encoding=encoding)
                            logger.info(
                                "Successfully read file with encoding",
                                file_path=file_path,
                                encoding=encoding,
                            )
                            break
                        except (UnicodeDecodeError, LookupError):
                            continue
                    if content is None:
                        # Last resort: try with 'replace' errors
                        content = path.read_text(encoding='utf-8', errors='replace')
                        logger.warning(
                            f"Read {file_path} with UTF-8 replace mode - some characters may be corrupted"
                        )
                if not content.strip():
                    continue

                # FIXED: Use ChunkerFactory.create() for each file instead of single AdaptiveChunker
                try:
                    # Create appropriate chunker for this specific file
                    file_chunker = ChunkerFactory.create(str(file_path), content)

                    # CRITICAL FIX: Add timeout to prevent workers hanging on chunking
                    file_chunks = await asyncio.wait_for(
                        file_chunker.chunk(content, str(file_path)),
                        timeout=30.0,  # 30 seconds max per file
                    )
                    chunks.extend(file_chunks)
                    continue
                except asyncio.TimeoutError:
                    logger.warning(
                        "ChunkerFactory timeout for file", file_path=file_path, timeout=30
                    )
                except Exception as e:
                    logger.warning(
                        "ChunkerFactory failed for file", file_path=file_path, error=str(e)
                    )

                # Fallback a DefaultChunker solo si ChunkerFactory falla
                try:
                    language = self._detect_language(path)
                    from acolyte.rag.chunking.languages.default import DefaultChunker

                    default_chunker = DefaultChunker(language)
                    # CRITICAL FIX: Add timeout to DefaultChunker fallback too
                    file_chunks = await asyncio.wait_for(
                        default_chunker.chunk(content, str(file_path)),
                        timeout=30.0,  # 30 seconds max per file
                    )
                    chunks.extend(file_chunks)
                    logger.info("DefaultChunker fallback succeeded for file", file_path=file_path)
                except asyncio.TimeoutError:
                    logger.error("DefaultChunker timeout for file", file_path=file_path, timeout=30)
                    self._failed_files.append(
                        {
                            'file': str(file_path),
                            'error': 'DefaultChunker timeout after 30s',
                            'stage': 'chunking',
                        }
                    )
                    continue
                except Exception as e2:
                    logger.error(
                        "Both chunkers failed for file", file_path=file_path, error=str(e2)
                    )
                    self._failed_files.append(
                        {'file': str(file_path), 'error': str(e2), 'stage': 'chunking'}
                    )
                    continue
            except Exception as e:
                logger.error("Failed to read file", file_path=file_path, error=str(e))
                self._failed_files.append(
                    {'file': str(file_path), 'error': str(e), 'stage': 'read'}
                )
        return chunks

    def _detect_chunk_type(self, content: str, file_extension: str) -> ChunkType:
        """
        Detect chunk type based on its content and extension.

        Uses patterns to identify the 18 ChunkType types.
        """
        content_lower = content.lower()

        # Patterns to detect types
        # NAMESPACE (check before CLASS to avoid false positives)
        if re.search(r"^\s*namespace\s+\w+", content, re.MULTILINE):
            return ChunkType.NAMESPACE

        # INTERFACE (check before CLASS)
        if re.search(r"^\s*interface\s+\w+", content, re.MULTILINE):
            return ChunkType.INTERFACE

        # CLASS (check after more specific patterns)
        if re.search(r"^\s*(class|struct)\s+\w+", content, re.MULTILINE):
            return ChunkType.CLASS

        # CONSTRUCTOR
        if re.search(r"def\s+__init__\s*\(", content) or re.search(r"constructor\s*\(", content):
            return ChunkType.CONSTRUCTOR

        # FUNCTION
        if re.search(r"\b(def|function|func|fn)\s+\w+\s*\(", content) or re.search(
            r"const\s+\w+\s*=\s*\(.*?\)\s*=>", content
        ):
            return ChunkType.FUNCTION

        # METHOD
        if re.search(r"^\s{4,}(def|function|func)\s+\w+\s*\(", content, re.MULTILINE):
            return ChunkType.METHOD

        # PROPERTY
        if (
            re.search(r"@property", content)
            or re.search(r"get\s+\w+\s*\(\s*\)", content)
            or re.search(r"set\s+\w+\s*\(", content)
        ):
            return ChunkType.PROPERTY

        # IMPORTS (check before MODULE - short import sections)
        if (
            re.search(r"^(import|from|require|use|include)", content, re.MULTILINE)
            and content.count("\n") < 20
        ):  # Short import section
            return ChunkType.IMPORTS

        # MODULE
        if file_extension in [".py", ".js", ".ts"] and re.search(
            r"^\s*(import|from|export|module)", content, re.MULTILINE
        ):
            return ChunkType.MODULE

        # CONSTANTS
        if re.search(r"^[A-Z_]+\s*=", content, re.MULTILINE) or re.search(
            r"^\s*const\s+[A-Z_]+", content, re.MULTILINE
        ):
            return ChunkType.CONSTANTS

        # TYPES
        if (
            re.search(r"^\s*(type|typedef|interface)\s+", content, re.MULTILINE)
            or file_extension in [".ts", ".tsx"]
            and "type " in content
        ):
            return ChunkType.TYPES

        # TESTS
        if (
            re.search(r"(test_|test\(|describe\(|it\(|@Test)", content)
            or "unittest" in content
            or "pytest" in content
        ):
            return ChunkType.TESTS

        # README
        if file_extension in [".md", ".rst"] and "readme" in content_lower:
            return ChunkType.README

        # DOCSTRING
        if (
            content.strip().startswith('"""')
            or content.strip().startswith("'''")
            or re.search(r"/\*\*[\s\S]*?\*/", content)
        ):
            return ChunkType.DOCSTRING

        # COMMENT
        if (
            content.strip().startswith("#")
            or content.strip().startswith("//")
            or content.strip().startswith("/*")
        ):
            return ChunkType.COMMENT

        # SUMMARY (for documentation files)
        if file_extension in [".md", ".rst", ".txt"] and len(content) < 500:
            return ChunkType.SUMMARY

        # Default
        return ChunkType.UNKNOWN

    def _infer_document_type(self, path: Path) -> DocumentType:
        """Infer document type by extension."""
        # Get file category from FileTypeDetector
        category = FileTypeDetector.get_category(path)

        # Map FileCategory to DocumentType
        category_to_doc_type = {
            FileCategory.CODE: DocumentType.CODE,
            FileCategory.DOCUMENTATION: DocumentType.MARKDOWN,
            FileCategory.CONFIGURATION: DocumentType.CONFIG,
            FileCategory.DATA: DocumentType.DATA,
            FileCategory.OTHER: DocumentType.OTHER,
        }

        return category_to_doc_type.get(category, DocumentType.OTHER)

    def _detect_language(self, path: Path) -> str:
        """Detect language by extension."""
        return FileTypeDetector.get_language(path)

    def _prepare_weaviate_object(
        self, chunk: Chunk, enrichment_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare object for Weaviate combining chunk and metadata."""
        # Chunk fields
        # Handle chunk_type carefully - can be None, ChunkType enum, or string
        chunk_type = getattr(chunk.metadata, "chunk_type", ChunkType.UNKNOWN)

        # FIX: Handle both enum and string cases
        if isinstance(chunk_type, ChunkType):
            # Already an enum - use its value and convert to uppercase
            chunk_type_str = chunk_type.value.upper()
        elif isinstance(chunk_type, str):
            # String value - try to convert back to enum, then get uppercase value
            try:
                # Try to find matching enum value
                for enum_item in ChunkType:
                    if enum_item.value == chunk_type:
                        chunk_type_str = enum_item.value.upper()
                        break
                else:
                    # No matching enum found - use UNKNOWN
                    chunk_type_str = ChunkType.UNKNOWN.value.upper()
            except Exception:
                chunk_type_str = ChunkType.UNKNOWN.value.upper()
        else:
            # Neither enum nor string - use UNKNOWN
            chunk_type_str = ChunkType.UNKNOWN.value.upper()

        weaviate_obj = {
            "content": chunk.content,
            "file_path": getattr(chunk.metadata, "file_path", ""),
            "chunk_type": chunk_type_str,
            "chunk_name": getattr(chunk.metadata, "name", ""),
            "language": getattr(chunk.metadata, "language", "unknown"),
            "start_line": getattr(chunk.metadata, "start_line", 0),
            "end_line": getattr(chunk.metadata, "end_line", 0),
        }

        # Enriched metadata (flatten)
        git_metadata = enrichment_metadata.get("git", {})
        if git_metadata:
            weaviate_obj.update(
                {
                    "git_last_author": git_metadata.get("last_author"),
                    "git_last_modified": git_metadata.get("last_modified"),
                    "git_stability_score": git_metadata.get("stability_score", 0),
                    "git_commit_hash": git_metadata.get("commit_hash"),
                }
            )

        pattern_metadata = enrichment_metadata.get("patterns", {})
        if pattern_metadata:
            weaviate_obj.update(
                {
                    "pattern_is_test": pattern_metadata.get("is_test_code", False),
                    "pattern_has_todo": pattern_metadata.get("has_todo", False),
                    "pattern_complexity": pattern_metadata.get("complexity", "medium"),
                }
            )

        # Indexing timestamp
        weaviate_obj["indexed_at"] = utc_now_iso()

        return weaviate_obj

    async def _index_to_weaviate(self, data_object: Dict[str, Any], vector: Any) -> None:
        """Index object in Weaviate with optional vector."""
        if not self.weaviate:
            return

        try:
            if vector is not None:
                # Import EmbeddingVector only when needed
                from acolyte.embeddings.types import EmbeddingVector

                # Handle different vector types
                if isinstance(vector, EmbeddingVector):
                    vector_list = vector.to_weaviate()
                elif hasattr(vector, "to_weaviate"):
                    vector_list = vector.to_weaviate()
                else:
                    vector_list = list(vector)

                self.weaviate.data_object.create(
                    class_name="CodeChunk", data_object=data_object, vector=vector_list
                )
            else:
                # Create without vector - Weaviate may generate if configured
                self.weaviate.data_object.create(class_name="CodeChunk", data_object=data_object)
        except Exception as e:
            logger.error("Failed to index to Weaviate", class_name="CodeChunk", error=str(e))
            raise ExternalServiceError(f"Failed to index to Weaviate: {str(e)}") from e

    async def _notify_progress(
        self,
        progress: Dict[str, Any],
        task_id: Optional[str] = None,
        files_skipped: int = 0,
        chunks_created: int = 0,
        embeddings_generated: int = 0,
        errors_count: int = 0,
        # Optional batch-specific parameters (for backward compatibility)
        batch_num: Optional[int] = None,
        total_batches: Optional[int] = None,
        files_in_batch: Optional[int] = None,
        batch_status: Optional[str] = None,
        estimated_remaining_seconds: Optional[float] = None,
    ):
        """
        Unified progress notification for both regular and batch indexing.

        Publishes ProgressEvent that can be consumed by:
        - WebSocketManager to update UI in real time
        - Other services that need to monitor indexing
        - Metrics system for tracking

        Args:
            progress: Object with progress information
            task_id: Optional task ID for WebSocket filtering
            files_skipped: Number of files skipped by filters
            chunks_created: Total chunks created so far
            embeddings_generated: Total embeddings generated
            errors_count: Number of errors found
            batch_num: Optional batch number for batch processing
            total_batches: Optional total batches for batch processing
            files_in_batch: Optional files in current batch
            batch_status: Optional batch status
            estimated_remaining_seconds: Optional time estimate
        """
        try:
            # Build enhanced message with batch context if available
            base_message = progress.get('current_file', '')
            if batch_num and total_batches:
                enhanced_message = f"[Batch {batch_num}/{total_batches}] {base_message}"
                operation = "batch_indexing_files"
            else:
                enhanced_message = f"Processing: {base_message}"
                operation = "indexing_files"

            # Prepare batch metadata for type-safe event creation
            batch_metadata = {}
            if batch_num is not None:
                batch_metadata["batch_num"] = batch_num
            if total_batches is not None:
                batch_metadata["total_batches"] = total_batches
            if files_in_batch is not None:
                batch_metadata["files_in_batch"] = files_in_batch
            if batch_status is not None:
                batch_metadata["batch_status"] = batch_status
            if estimated_remaining_seconds is not None:
                batch_metadata["estimated_remaining_seconds"] = estimated_remaining_seconds

            # Create progress event with complete statistics and batch metadata
            progress_event = ProgressEvent(
                source="indexing_service",
                operation=operation,
                current=progress["processed_files"],
                total=progress["total_files"],
                message=enhanced_message,
                task_id=task_id,
                files_skipped=files_skipped,
                chunks_created=chunks_created,
                embeddings_generated=embeddings_generated,
                errors=errors_count,
                current_file=progress.get('current_file', ''),
                metadata=batch_metadata,
            )

            # Publish event
            await event_bus.publish(progress_event)

            # Log only at significant intervals (every 10% or every 10 files)
            if (
                progress["processed_files"] % 10 == 0
                or progress["processed_files"] == progress["total_files"]
                or int(progress.get("percentage", 0)) % 10 == 0
            ):
                log_method = "Batch indexing progress" if batch_num else "Indexing progress"
                logger.info(
                    log_method,
                    processed=progress["processed_files"],
                    total=progress["total_files"],
                    percentage=f"{progress.get('percentage', 0):.1f}%",
                    current_file=progress["current_file"],
                    task_id=task_id,
                    batch_num=batch_num,
                    total_batches=total_batches,
                    batch_status=batch_status,
                    estimated_remaining_minutes=(
                        round(estimated_remaining_seconds / 60, 1)
                        if estimated_remaining_seconds
                        else None
                    ),
                )

        except Exception as e:
            # Don't fail indexing due to notification errors
            logger.warning("Failed to notify progress", error=str(e))

    # ============================================================================
    # ADDITIONAL METHODS FOR API
    # ============================================================================

    async def estimate_files(
        self,
        root: Path,
        patterns: List[str],
        exclude_patterns: List[str],
        respect_gitignore: bool = True,
        respect_acolyteignore: bool = True,
    ) -> int:
        """
        Estimate how many files would be indexed.

        PURPOSE: Dashboard UX - show estimated time before indexing.

        Args:
            root: Project root directory
            patterns: File patterns to include (*.py, *.js, etc.)
            exclude_patterns: Patterns to exclude
            respect_gitignore: Whether to respect .gitignore
            respect_acolyteignore: Whether to respect .acolyteignore

        Returns:
            Estimated number of files that would be indexed
        """
        try:
            start_time = utc_now()
            logger.info(
                "Estimating files for indexing", root=str(root), patterns_count=len(patterns)
            )

            # Collect files matching patterns
            candidate_files = []

            for pattern in patterns:
                if pattern.startswith("*."):
                    # Extension pattern: *.py -> **/*.py
                    ext = pattern[2:]
                    matches = list(root.rglob(f"*.{ext}"))
                    candidate_files.extend([str(f) for f in matches])
                else:
                    # Direct pattern
                    matches = list(root.rglob(pattern))
                    candidate_files.extend([str(f) for f in matches])

            # Remove duplicates
            candidate_files = list(set(candidate_files))

            # Aplicar exclude_patterns adicionales
            if exclude_patterns:
                exclude_regexes = []
                for pattern in exclude_patterns:
                    # Convert glob patterns to regex (reuse _glob_to_regex logic)
                    try:
                        exclude_regex = self._glob_to_regex(pattern)
                        exclude_regexes.append(exclude_regex)
                    except re.error as e:
                        logger.warning("Invalid exclude pattern", pattern=pattern, error=str(e))
                        continue

                # Filtrar archivos que coincidan con exclude_patterns
                filtered_candidates = []
                for file_path in candidate_files:
                    file_str = str(file_path).replace('\\', '/')
                    if not any(r.search(file_str) for r in exclude_regexes):
                        filtered_candidates.append(file_path)
                candidate_files = filtered_candidates

            # Apply filters (same logic as _filter_files but without detailed logs)
            estimated_count = 0

            for file_path in candidate_files:
                path = Path(file_path)

                # Verify it exists and is not a directory
                if not path.exists() or path.is_dir():
                    continue

                # Verify size
                try:
                    size_mb = path.stat().st_size / (1024 * 1024)
                    if size_mb > self.max_file_size_mb:
                        continue
                except OSError:
                    continue

                # Verify ignore patterns
                if self._should_ignore(str(path)):
                    continue

                # Verify supported extension
                if not self._is_supported_file(path):
                    continue

                estimated_count += 1

            logger.info(
                "File estimation completed",
                candidates=len(candidate_files),
                estimated=estimated_count,
                filter_rate=f"{(1 - estimated_count/max(len(candidate_files), 1))*100:.1f}%",
            )

            self.metrics.gauge("indexing.estimated_files", estimated_count)

            # Record timing
            elapsed_ms = (utc_now() - start_time).total_seconds() * 1000
            self.metrics.record("indexing.estimate_files_ms", elapsed_ms)

            return estimated_count

        except Exception as e:
            logger.error("Failed to estimate files", error=str(e))
            # Return conservative estimate in case of error
            return 100

    async def remove_file(self, file_path: str) -> bool:
        """
        Remove a file from the search index.

        PURPOSE: Keep index clean when files are removed from the project.

        Args:
            file_path: Path of the file to remove from index

        Returns:
            True if successfully removed, False otherwise
        """
        try:
            start_time = utc_now()
            logger.info("Removing file from index", file_path=file_path)

            if not self.weaviate or not WEAVIATE_AVAILABLE:
                logger.warning("Weaviate not available for file removal")
                return False

            # Find objects in Weaviate that correspond to this file
            try:
                # Query to find chunks for this file
                where_filter = {
                    "path": ["file_path"],
                    "operator": "Equal",
                    "valueText": file_path,
                }

                result = (
                    self.weaviate.query.get("CodeChunk", ["file_path"])
                    .with_where(where_filter)
                    .with_additional(["id"])
                    .do()
                )
                from typing import cast, List, Dict, Any

                chunks_to_delete = cast(
                    List[Dict[str, Any]], result.get("data", {}).get("Get", {}).get("CodeChunk", [])
                )
                logger.info("[TRACE] Weaviate remove_file path executed")
                if chunks_to_delete:
                    deleted_count = 0
                    for chunk_data in chunks_to_delete:
                        chunk_id = chunk_data.get("_additional", {}).get("id")
                        if chunk_id:
                            try:
                                self.weaviate.data_object.delete(chunk_id, class_name="CodeChunk")
                                deleted_count += 1
                            except Exception as e:
                                logger.warning(
                                    "Failed to delete chunk", chunk_id=chunk_id, error=str(e)
                                )
                    logger.info(
                        "File removal completed",
                        file_path=file_path,
                        chunks_deleted=deleted_count,
                    )
                    self.metrics.increment("indexing.files_removed")
                    self.metrics.increment("indexing.chunks_removed", deleted_count)
                    elapsed_ms = (utc_now() - start_time).total_seconds() * 1000
                    self.metrics.record("indexing.remove_file_ms", elapsed_ms)
                    return deleted_count > 0
                else:
                    logger.info("No chunks found for file", file_path=file_path)
                    elapsed_ms = (utc_now() - start_time).total_seconds() * 1000
                    self.metrics.record("indexing.remove_file_ms", elapsed_ms)
                    return True

            except Exception as e:
                logger.error(
                    "Failed to query/delete from Weaviate", file_path=file_path, error=str(e)
                )
                return False

        except Exception as e:
            logger.error("Failed to remove file", file_path=file_path, error=str(e))
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """
        Get indexing statistics for the dashboard.

        PURPOSE: Show metrics in the web dashboard.

        Returns:
            Dict with indexing statistics:
            - total_files: Unique indexed files
            - total_chunks: Total chunks in Weaviate
            - languages: Distribution by language
            - chunk_types: Distribution by chunk type
            - last_indexed: Last indexing timestamp
            - index_size_estimate: Index size estimate
        """
        try:
            start_time = utc_now()
            logger.info("Getting indexing statistics")

            stats = {
                "total_files": 0,
                "total_chunks": 0,
                "languages": {},
                "chunk_types": {},
                "last_indexed": None,
                "index_size_estimate_mb": 0.0,
                "weaviate_available": WEAVIATE_AVAILABLE and self.weaviate is not None,
            }

            if not self.weaviate or not WEAVIATE_AVAILABLE:
                logger.warning("Weaviate not available for stats")
                return stats

            try:
                # Get total chunk count
                count_result = self.weaviate.query.aggregate("CodeChunk").with_meta_count().do()

                if "data" in count_result and "Aggregate" in count_result["data"]:
                    aggregate_data = count_result["data"]["Aggregate"].get("CodeChunk", [{}])[0]
                    stats["total_chunks"] = aggregate_data.get("meta", {}).get("count", 0)

                # Get distribution by language
                lang_result = (
                    self.weaviate.query.aggregate("CodeChunk")
                    .with_group_by_filter(["language"])
                    .with_meta_count()
                    .do()
                )
                from typing import cast, List, Dict, Any

                lang_groups = cast(
                    List[Dict[str, Any]],
                    lang_result.get("data", {}).get("Aggregate", {}).get("CodeChunk", []),
                )
                for group in lang_groups:
                    if "groupedBy" in group and "value" in group["groupedBy"]:
                        language = group["groupedBy"]["value"]
                        count = group.get("meta", {}).get("count", 0)
                        if language and count > 0:
                            stats["languages"][language] = count

                # Get distribution by chunk type
                type_result = (
                    self.weaviate.query.aggregate("CodeChunk")
                    .with_group_by_filter(["chunk_type"])
                    .with_meta_count()
                    .do()
                )
                type_groups = cast(
                    List[Dict[str, Any]],
                    type_result.get("data", {}).get("Aggregate", {}).get("CodeChunk", []),
                )
                for group in type_groups:
                    if "groupedBy" in group and "value" in group["groupedBy"]:
                        chunk_type = group["groupedBy"]["value"]
                        count = group.get("meta", {}).get("count", 0)
                        if chunk_type and count > 0:
                            stats["chunk_types"][chunk_type] = count

                # Get unique files (approximated by unique file_path)
                # Note: Weaviate doesn't have native DISTINCT, so we estimate
                if stats["total_chunks"] > 0:
                    # Estimation based on average chunks per file
                    avg_chunks_per_file = 10  # Conservative value
                    stats["total_files"] = max(1, stats["total_chunks"] // avg_chunks_per_file)

                # Get last indexing (from metrics if available)
                # For now, use current timestamp as placeholder
                stats["last_indexed"] = utc_now_iso()

                # Estimate index size (approximated)
                # Each chunk ~2KB average (content + metadata + vector)
                stats["index_size_estimate_mb"] = round((stats["total_chunks"] * 2) / 1024, 2)

                logger.info(
                    "Indexing stats retrieved",
                    total_chunks=stats["total_chunks"],
                    languages=len(stats["languages"]),
                    types=len(stats["chunk_types"]),
                )

                self.metrics.gauge("indexing.indexed_chunks_total", stats["total_chunks"])
                self.metrics.gauge("indexing.indexed_files_estimated", stats["total_files"])

            except Exception as e:
                logger.error("Failed to query Weaviate for stats", error=str(e))
                # Return partial stats instead of failing completely

            # Record timing
            elapsed_ms = (utc_now() - start_time).total_seconds() * 1000
            self.metrics.record("indexing.get_stats_ms", elapsed_ms)

            return stats

        except Exception as e:
            logger.error("Failed to get indexing stats", error=str(e))
            return {
                "total_files": 0,
                "total_chunks": 0,
                "languages": {},
                "chunk_types": {},
                "last_indexed": None,
                "index_size_estimate_mb": 0.0,
                "error": str(e),
            }

    async def rename_file(self, old_path: str, new_path: str) -> bool:
        """
        Update references of a renamed file in the index.

        PURPOSE: Preserve history when files are moved/renamed.

        Args:
            old_path: Previous file path
            new_path: New file path

        Returns:
            True if successfully updated, False otherwise
        """
        try:
            start_time = utc_now()
            logger.info("Renaming file in index", old_path=old_path, new_path=new_path)

            if not self.weaviate or not WEAVIATE_AVAILABLE:
                logger.warning("Weaviate not available for file renaming")
                return False

            # Find objects in Weaviate that correspond to the old file
            try:
                where_filter = {
                    "path": ["file_path"],
                    "operator": "Equal",
                    "valueText": old_path,
                }

                result = (
                    self.weaviate.query.get("CodeChunk", ["file_path"])
                    .with_where(where_filter)
                    .with_additional(["id"])
                    .do()
                )
                from typing import cast, List, Dict, Any

                chunks_to_update = cast(
                    List[Dict[str, Any]], result.get("data", {}).get("Get", {}).get("CodeChunk", [])
                )
                logger.info("[TRACE] Weaviate rename_file path executed")
                if chunks_to_update:
                    updated_count = 0
                    for chunk_data in chunks_to_update:
                        chunk_id = chunk_data.get("_additional", {}).get("id")
                        if chunk_id:
                            try:
                                self.weaviate.data_object.update(
                                    data_object={"file_path": new_path},
                                    class_name="CodeChunk",
                                    uuid=chunk_id,
                                )
                                updated_count += 1
                            except Exception as e:
                                logger.warning(
                                    "Failed to update chunk", chunk_id=chunk_id, error=str(e)
                                )
                    logger.info(
                        "File rename completed",
                        old_path=old_path,
                        new_path=new_path,
                        chunks_updated=updated_count,
                    )
                    self.metrics.increment("indexing.files_renamed")
                    self.metrics.increment("indexing.chunks_updated", updated_count)
                    elapsed_ms = (utc_now() - start_time).total_seconds() * 1000
                    self.metrics.record("indexing.rename_file_ms", elapsed_ms)
                    return updated_count > 0
                else:
                    logger.info("No chunks found for old file path", old_path=old_path)
                    return True

            except Exception as e:
                logger.error(
                    "Failed to query/update Weaviate",
                    old_path=old_path,
                    new_path=new_path,
                    error=str(e),
                )
                return False

        except Exception as e:
            logger.error(
                "Failed to rename file", old_path=old_path, new_path=new_path, error=str(e)
            )
            return False

    def is_supported_file(self, path: Path) -> bool:
        """Check if the file is of a supported type (public method)."""
        return self._is_supported_file(path)

    def should_ignore(self, file_path: str) -> bool:
        """Check if a file should be ignored (public method)."""
        return self._should_ignore(file_path)

    def _generate_error_summary(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a human-readable summary of indexing errors."""
        summary = {"total_errors": len(errors), "by_type": {}, "by_file": {}, "sample_errors": []}

        # Categorize errors
        for error in errors:
            # By error type
            error_type = error.get("error_type", "Unknown")
            if error_type not in summary["by_type"]:
                summary["by_type"][error_type] = 0
            summary["by_type"][error_type] += 1

            # By file (if it's a file-level error)
            if "file" in error:
                file_path = error["file"]
                if file_path not in summary["by_file"]:
                    summary["by_file"][file_path] = []
                summary["by_file"][file_path].append(
                    {"error": error.get("error", "Unknown error"), "type": error_type}
                )

        # Include sample of first 5 errors for debugging
        summary["sample_errors"] = errors[:5]

        return summary

    @property
    def is_indexing(self):
        """Indica si el servicio está indexando actualmente."""
        return self._is_indexing

    def _is_batch_paused(self, task_id: str) -> bool:
        """Check if batch processing is paused for a task."""
        try:
            # Check if task is paused using progress tracker (same logic as API)
            from acolyte.core.progress import progress_tracker

            task_info = progress_tracker.get_task(task_id)
            if not task_info:
                return False
            return task_info.stats.get("is_paused", False)
        except (ImportError, AttributeError) as e:
            # Fallback if progress tracker is not available or has issues
            logger.debug(f"Could not check pause status: {e}")
            return False

    def _update_progress_tracker(
        self, task_id: str, processed: int, total: int, message: str, extra_data: Dict[str, Any]
    ):
        """Update progress tracker with current status. [STUB - Phase 3]"""
        pass

    async def _clear_old_checkpoints(self, days: int):
        """Clear old checkpoint data. [STUB - Phase 3]"""
        pass

    async def _cleanup_corrupted_state(self):
        """Clean up any corrupted state from interrupted operations. [STUB - Phase 3]"""
        pass

    async def _save_progress(self, task_id: str, progress_data: Dict[str, Any]):
        """Save indexing progress to job_states table.

        Uses job_states table directly for structured job tracking.
        This provides better querying capabilities than key-value storage.
        """
        try:
            from acolyte.core.database import get_db_manager, FetchType

            db = get_db_manager()

            # Determine job type based on task_id prefix
            job_type = 'reindexing' if task_id.startswith('reinx_') else 'indexing'

            # Check if job already exists
            existing = await db.execute_async(
                "SELECT id FROM job_states WHERE job_id = ?", (task_id,), FetchType.ONE
            )

            if existing.data:
                # Update existing job
                await db.execute_async(
                    """
                    UPDATE job_states 
                    SET status = ?,
                        progress = ?,
                        total = ?,
                        current_item = ?,
                        metadata = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE job_id = ?
                    """,
                    (
                        'running',
                        progress_data.get('processed_files', 0),
                        progress_data.get('total_files', 0),
                        progress_data.get('current_file', ''),
                        json.dumps(progress_data),
                        task_id,
                    ),
                    FetchType.NONE,
                )
            else:
                # Create new job
                await db.execute_async(
                    """
                    INSERT INTO job_states (
                        job_type, job_id, status, progress, total,
                        current_item, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        job_type,
                        task_id,
                        'running',
                        progress_data.get('processed_files', 0),
                        progress_data.get('total_files', 0),
                        progress_data.get('current_file', ''),
                        json.dumps(progress_data),
                    ),
                    FetchType.NONE,
                )
        except Exception as e:
            # Not critical - indexing can continue without checkpoint
            logger.warning("Error saving indexing progress", task_id=task_id, error=str(e))

    async def _load_progress(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Load saved indexing progress from job_states table."""
        try:
            from acolyte.core.database import get_db_manager, FetchType

            db = get_db_manager()

            result = await db.execute_async(
                "SELECT metadata FROM job_states WHERE job_id = ? AND status = 'running'",
                (task_id,),
                FetchType.ONE,
            )

            if result.data and isinstance(result.data, dict):
                metadata_str = result.data.get('metadata')
                if metadata_str:
                    progress = json.loads(metadata_str)
                    # Validar integridad
                    required_fields = [
                        "task_id",
                        "status",
                        "total_files",
                        "processed_files",
                        "files_pending",
                    ]
                    if not progress or not all(f in progress for f in required_fields):
                        logger.warning(
                            f"Checkpoint corrupted or incomplete for {task_id}, ignoring."
                        )
                        return None
                    return progress
            return None
        except Exception as e:
            logger.warning("Error loading indexing progress", task_id=task_id, error=str(e))
            return None

    async def _clear_progress(self, task_id: str):
        """Mark job as completed in job_states table."""
        try:
            from acolyte.core.database import get_db_manager, FetchType

            db = get_db_manager()

            await db.execute_async(
                """
                UPDATE job_states 
                SET status = 'completed',
                    completed_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE job_id = ?
                """,
                (task_id,),
                FetchType.NONE,
            )
        except Exception as e:
            logger.warning("Error clearing indexing progress", task_id=task_id, error=str(e))

    async def list_resumable_tasks(self) -> List[Dict[str, Any]]:
        """List all resumable indexing tasks from job_states table."""
        try:
            from acolyte.core.database import get_db_manager, FetchType

            db = get_db_manager()

            result = await db.execute_async(
                """
                SELECT job_id, job_type, progress, total, current_item, 
                       started_at, updated_at, metadata
                FROM job_states 
                WHERE status = 'running' 
                  AND job_type IN ('indexing', 'reindexing')
                ORDER BY updated_at DESC
                """,
                (),
                FetchType.ALL,
            )

            tasks = []
            if result.data:
                for row in result.data:
                    row = cast(Dict[str, Any], row)
                    metadata = {}
                    if row.get('metadata'):
                        try:
                            metadata = json.loads(row['metadata'])
                        except json.JSONDecodeError:
                            pass

                    tasks.append(
                        {
                            "task_id": row["job_id"],
                            "job_type": row["job_type"],
                            "started_at": row["started_at"],
                            "total_files": row["total"],
                            "processed_files": row["progress"],
                            "pending_files": metadata.get("total_files", 0) - row["progress"],
                            "last_checkpoint": row["updated_at"],
                            "current_file": row["current_item"],
                        }
                    )

            return tasks
        except Exception as e:
            logger.error("Error listing resumable tasks", error=str(e))
            return []

    async def shutdown(self):
        """Gracefully shutdown the indexing service and cleanup resources."""
        logger.info("Shutting down IndexingService")

        # Cancel any pending cleanup tasks
        if self._cleanup_tasks:
            logger.info(f"Cancelling {len(self._cleanup_tasks)} pending cleanup tasks")
            for task in self._cleanup_tasks:
                if not task.done():
                    task.cancel()

            # Wait for cancellation to complete
            if self._cleanup_tasks:
                try:
                    await asyncio.gather(*self._cleanup_tasks, return_exceptions=True)
                except Exception as e:
                    logger.warning("Error waiting for cleanup tasks cancellation", error=str(e))

            self._cleanup_tasks.clear()

        # Shutdown worker pool if exists
        if self._worker_pool:
            try:
                await self._worker_pool.shutdown()
                self._worker_pool = None
                logger.info("Worker pool shutdown complete")
            except Exception as e:
                logger.error("Error shutting down worker pool", error=str(e))

        # Wait for any ongoing indexing to complete
        if self._is_indexing:
            logger.info("Waiting for ongoing indexing to complete...")
            # Give it max 30 seconds to complete
            for _ in range(30):
                if not self._is_indexing:
                    break
                await asyncio.sleep(1)

            if self._is_indexing:
                logger.warning("Indexing still in progress after 30s, forcing shutdown")

        # Close embeddings cache BEFORE database to prevent access violations
        try:
            if self.embeddings is not None:
                if hasattr(self.embeddings, 'cache') and hasattr(self.embeddings.cache, 'close'):
                    self.embeddings.cache.close()
                    logger.info("Embeddings cache closed in shutdown")
        except Exception as e:
            logger.warning("Error closing embeddings cache in shutdown", error=str(e))

        # 🔧 REMOVED: Aggressive database closing that caused Windows fatal exceptions in shutdown
        # The aggressive close() calls were causing race conditions with concurrent database operations
        # DatabaseManager handles connection management automatically and safely during application lifecycle
        # Manual closing in shutdown() is unnecessary and dangerous

        logger.info("IndexingService shutdown complete")
