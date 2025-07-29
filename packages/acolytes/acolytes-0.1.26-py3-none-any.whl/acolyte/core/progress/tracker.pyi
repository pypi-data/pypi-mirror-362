"""Progress tracker for indexing and other long-running tasks - Type stubs."""

import time
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field

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

    def to_dict(self) -> Dict[str, Any]: ...

class ProgressTracker:
    """
    Centralized progress tracking for all long-running tasks.
    Thread-safe and accessible from anywhere in the application.
    """

    def start_task(self, task_id: str, total: int, message: str = "Starting...") -> TaskInfo: ...
    def update_task(
        self,
        task_id: str,
        current: Optional[int] = None,
        message: Optional[str] = None,
        stats: Optional[Dict[str, Any]] = None,
        status: Optional[TaskStatus] = None,
    ) -> Optional[TaskInfo]: ...
    def complete_task(self, task_id: str, message: str = "Completed") -> Optional[TaskInfo]: ...
    def fail_task(self, task_id: str, error: str) -> Optional[TaskInfo]: ...
    def get_task(self, task_id: str) -> Optional[TaskInfo]: ...
    def get_active_tasks(self) -> List[TaskInfo]: ...
    def cancel_task(self, task_id: str) -> Optional[TaskInfo]: ...
    def get_memory_stats(self) -> Dict[str, Any]: ...
    async def shutdown(self) -> None: ...

# Global instance
progress_tracker: ProgressTracker
