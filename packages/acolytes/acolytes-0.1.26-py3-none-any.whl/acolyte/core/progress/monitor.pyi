"""Progress monitoring utilities for CLI and other clients - Type stubs."""

from typing import Optional, Any, Dict
from rich.progress import Progress
from rich.console import Console

class ProgressMonitor:
    """
    Unified progress monitoring with WebSocket + HTTP fallback.
    Provides a clean interface for CLI and other clients.
    """

    backend_port: int
    console: Console
    websocket_retries: int
    websocket_timeout: int
    polling_interval: int

    def __init__(self, backend_port: int, console: Optional[Console] = None) -> None: ...
    async def monitor_task(
        self, task_id: str, total_files: int = 0, verbose: bool = False
    ) -> Dict[str, Any]: ...
    async def _get_initial_status(self, task_id: str) -> Optional[Dict[str, Any]]: ...
    async def _try_websocket_monitoring(
        self, task_id: str, progress: Progress, task: Any, verbose: bool
    ) -> Optional[Dict[str, Any]]: ...
    async def _handle_websocket_messages(
        self, websocket: Any, progress: Progress, task: Any, verbose: bool
    ) -> Dict[str, Any]: ...
    async def _http_polling_fallback(
        self, task_id: str, progress: Progress, task: Any, verbose: bool
    ) -> Dict[str, Any]: ...
    def display_final_stats(self, stats: Dict[str, Any], elapsed_time: float) -> None: ...
