"""
Progress tracker for indexing and other long-running tasks.
"""

import time
import asyncio
from typing import Dict, Any, Optional, List
from enum import Enum
from threading import Lock
from dataclasses import dataclass, field

from acolyte.core.logging import logger


class TaskStatus(Enum):
    """Task status enumeration."""

    STARTING = "starting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskInfo:
    """Information about a running task."""

    task_id: str
    status: TaskStatus
    current: int = 0
    total: int = 0
    message: str = "Initializing..."
    started_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    stats: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "current": self.current,
            "total": self.total,
            "message": self.message,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "stats": self.stats,
            "errors": self.errors,
            "progress_percent": round(
                (self.current / self.total * 100) if self.total > 0 else 0, 1
            ),
            "elapsed_seconds": int(time.time() - self.started_at),
            "files_per_second": (
                round(self.current / max(time.time() - self.started_at, 1), 2)
                if self.current > 0
                else 0
            ),
        }


class ProgressTracker:
    """
    Centralized progress tracking for all long-running tasks.
    Thread-safe and accessible from anywhere in the application.

    🔧 MEMORY LEAK PREVENTION:
    - Proactive cleanup every 5 minutes
    - Automatic cleanup of stale paused tasks (>6 hours)
    - Maximum task limit (1000 tasks)
    - Background cleanup task
    """

    def __init__(self):
        self._tasks: Dict[str, TaskInfo] = {}
        self._lock = Lock()
        self._cleanup_interval = 3600  # Clean up completed tasks after 1 hour
        self._proactive_cleanup_interval = 300  # Proactive cleanup every 5 minutes
        self._max_tasks = 1000  # Maximum tasks to prevent unbounded growth
        self._stale_pause_timeout = 21600  # 6 hours - cleanup stale paused tasks
        self._last_cleanup = time.time()
        self._last_proactive_cleanup = time.time()

        # Background cleanup task (optional - only start if asyncio loop is available)
        self._cleanup_task: Optional[asyncio.Task] = None
        self._start_background_cleanup()

    def _start_background_cleanup(self):
        """Start background cleanup task if asyncio loop is available."""
        try:
            loop = asyncio.get_running_loop()
            self._cleanup_task = loop.create_task(self._background_cleanup_loop())
            logger.debug("Background cleanup task started for ProgressTracker")
        except RuntimeError:
            # No event loop running, cleanup will be manual only
            logger.debug("No event loop available, using manual cleanup only")

    async def _background_cleanup_loop(self):
        """Background task that performs periodic cleanup."""
        while True:
            try:
                await asyncio.sleep(self._proactive_cleanup_interval)
                self._proactive_cleanup()
            except asyncio.CancelledError:
                logger.debug("Background cleanup task cancelled")
                break
            except Exception as e:
                logger.error("Error in background cleanup", error=str(e))

    def start_task(self, task_id: str, total: int, message: str = "Starting...") -> TaskInfo:
        """Start tracking a new task."""
        with self._lock:
            # 🔧 MEMORY LEAK FIX: Aggressive cleanup before adding new task
            self._cleanup_old_tasks()
            self._enforce_task_limit()

            task = TaskInfo(
                task_id=task_id, status=TaskStatus.STARTING, total=total, message=message
            )
            self._tasks[task_id] = task
            logger.info("Task started", task_id=task_id, total=total, active_tasks=len(self._tasks))

            return task

    def update_task(
        self,
        task_id: str,
        current: Optional[int] = None,
        message: Optional[str] = None,
        stats: Optional[Dict[str, Any]] = None,
        status: Optional[TaskStatus] = None,
    ) -> Optional[TaskInfo]:
        """Update task progress."""
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None

            if current is not None:
                task.current = current
            if message is not None:
                task.message = message
            if stats is not None:
                task.stats.update(stats)
            if status is not None:
                task.status = status
                if status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                    task.completed_at = time.time()

            task.updated_at = time.time()

            # Auto-update status to RUNNING if still STARTING and progress > 0
            if task.status == TaskStatus.STARTING and task.current > 0:
                task.status = TaskStatus.RUNNING

            return task

    def complete_task(self, task_id: str, message: str = "Completed") -> Optional[TaskInfo]:
        """Mark task as completed."""
        return self.update_task(task_id, status=TaskStatus.COMPLETED, message=message)

    def fail_task(self, task_id: str, error: str) -> Optional[TaskInfo]:
        """Mark task as failed."""
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                task.errors.append(error)
                task.status = TaskStatus.FAILED
                task.message = f"Failed: {error}"
                task.completed_at = time.time()
                logger.error("Task failed", task_id=task_id, error=error)
            return task

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        """Get task information."""
        with self._lock:
            # 🔧 MEMORY LEAK FIX: Opportunistic cleanup on reads
            if time.time() - self._last_proactive_cleanup > self._proactive_cleanup_interval:
                self._proactive_cleanup()
            return self._tasks.get(task_id)

    def get_active_tasks(self) -> List[TaskInfo]:
        """Get all active (not completed) tasks."""
        with self._lock:
            return [
                task
                for task in self._tasks.values()
                if task.status in [TaskStatus.STARTING, TaskStatus.RUNNING]
            ]

    def cancel_task(self, task_id: str) -> Optional[TaskInfo]:
        """Cancel a running task."""
        return self.update_task(task_id, status=TaskStatus.CANCELLED, message="Cancelled by user")

    def _cleanup_old_tasks(self):
        """Remove old completed tasks to prevent memory leak."""
        current_time = time.time()
        if current_time - self._last_cleanup < self._cleanup_interval:
            return

        # Remove tasks completed more than 1 hour ago
        cutoff_time = current_time - self._cleanup_interval
        tasks_to_remove = [
            task_id
            for task_id, task in self._tasks.items()
            if task.completed_at and task.completed_at < cutoff_time
        ]

        for task_id in tasks_to_remove:
            del self._tasks[task_id]

        if tasks_to_remove:
            logger.info("Cleaned up old completed tasks", count=len(tasks_to_remove))

        self._last_cleanup = current_time

    def _proactive_cleanup(self):
        """🔧 MEMORY LEAK FIX: Proactive cleanup of stale tasks."""
        current_time = time.time()
        if current_time - self._last_proactive_cleanup < self._proactive_cleanup_interval:
            return

        tasks_to_remove = []

        # 1. Remove old completed tasks (same as before)
        cutoff_time = current_time - self._cleanup_interval
        for task_id, task in self._tasks.items():
            if task.completed_at and task.completed_at < cutoff_time:
                tasks_to_remove.append(task_id)

        # 2. 🔧 NEW: Remove stale paused tasks (paused for >6 hours)
        stale_cutoff = current_time - self._stale_pause_timeout
        for task_id, task in self._tasks.items():
            if (
                task_id not in tasks_to_remove
                and task.stats.get("is_paused", False)
                and task.updated_at < stale_cutoff
            ):
                tasks_to_remove.append(task_id)
                logger.warning(
                    "Removing stale paused task",
                    task_id=task_id,
                    hours_stale=round((current_time - task.updated_at) / 3600, 1),
                )

        # 3. 🔧 NEW: Remove old RUNNING tasks that seem abandoned (>24 hours with no updates)
        abandoned_cutoff = current_time - 86400  # 24 hours
        for task_id, task in self._tasks.items():
            if (
                task_id not in tasks_to_remove
                and task.status == TaskStatus.RUNNING
                and task.updated_at < abandoned_cutoff
            ):
                tasks_to_remove.append(task_id)
                logger.warning(
                    "Removing abandoned running task",
                    task_id=task_id,
                    hours_abandoned=round((current_time - task.updated_at) / 3600, 1),
                )

        # Remove identified tasks
        for task_id in tasks_to_remove:
            del self._tasks[task_id]

        if tasks_to_remove:
            logger.info(
                "Proactive cleanup completed",
                removed_tasks=len(tasks_to_remove),
                active_tasks=len(self._tasks),
            )

        self._last_proactive_cleanup = current_time

    def _enforce_task_limit(self):
        """🔧 MEMORY LEAK FIX: Enforce maximum task limit."""
        if len(self._tasks) < self._max_tasks:
            return

        # Sort by update time, remove oldest tasks first
        sorted_tasks = sorted(self._tasks.items(), key=lambda x: x[1].updated_at)
        tasks_to_remove = sorted_tasks[
            : len(self._tasks) - self._max_tasks + 100
        ]  # Keep 100 buffer

        for task_id, task in tasks_to_remove:
            del self._tasks[task_id]
            logger.warning("Removed task due to limit", task_id=task_id, status=task.status.value)

        if tasks_to_remove:
            logger.warning(
                "Enforced task limit",
                removed_count=len(tasks_to_remove),
                current_count=len(self._tasks),
                max_limit=self._max_tasks,
            )

    def get_memory_stats(self) -> Dict[str, Any]:
        """🔧 NEW: Get memory usage statistics for monitoring."""
        with self._lock:
            status_counts = {}
            for task in self._tasks.values():
                status = task.status.value
                status_counts[status] = status_counts.get(status, 0) + 1

            current_time = time.time()
            return {
                "total_tasks": len(self._tasks),
                "status_breakdown": status_counts,
                "oldest_task_age_hours": (
                    round(
                        (current_time - min(task.started_at for task in self._tasks.values()))
                        / 3600,
                        1,
                    )
                    if self._tasks
                    else 0
                ),
                "last_cleanup_minutes_ago": round((current_time - self._last_cleanup) / 60, 1),
                "last_proactive_cleanup_minutes_ago": round(
                    (current_time - self._last_proactive_cleanup) / 60, 1
                ),
                "memory_usage_estimate_kb": len(self._tasks) * 2,  # Rough estimate: ~2KB per task
            }

    async def shutdown(self):
        """🔧 NEW: Graceful shutdown with cleanup."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            logger.debug("Background cleanup task stopped")

        with self._lock:
            tasks_count = len(self._tasks)
            self._tasks.clear()
            logger.info("ProgressTracker shutdown", tasks_cleared=tasks_count)


# Global instance
progress_tracker = ProgressTracker()
