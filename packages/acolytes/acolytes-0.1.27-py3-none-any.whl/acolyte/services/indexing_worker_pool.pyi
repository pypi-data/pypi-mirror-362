from typing import Any, Dict, List, Optional, Tuple
import asyncio
from acolyte.models.chunk import Chunk

class IndexingWorkerPool:
    indexing_service: Any
    num_workers: int
    config: Any
    metrics: Any
    perf_logger: Any
    _file_queue: asyncio.Queue
    _worker_tasks: List[asyncio.Task]
    _weaviate_clients: List[Any]
    _embeddings_semaphore: asyncio.Semaphore
    _worker_results: Dict[int, Dict[str, Any]]
    _shutdown_event: asyncio.Event
    _initialized: bool

    def __init__(
        self, indexing_service: Any, num_workers: int = ..., embeddings_semaphore_size: int = ...
    ) -> None: ...
    async def initialize(self) -> None: ...
    async def _create_weaviate_clients(self) -> None: ...
    async def process_files(
        self, files: List[str], batch_size: int = ..., trigger: str = ...
    ) -> Dict[str, Any]: ...
    async def _worker(self, worker_id: int) -> None: ...
    async def _process_file_batch(
        self, worker_id: int, files: List[str], trigger: str, batch_inserter: Optional[Any]
    ) -> Dict[str, Any]: ...
    async def _enrich_chunks(
        self, chunks: List[Chunk], trigger: str
    ) -> List[Tuple[Chunk, Dict[str, Any]]]: ...
    async def _generate_embeddings(
        self, worker_id: int, enriched_tuples: List[Tuple[Chunk, Dict[str, Any]]]
    ) -> List[Optional[Any]]: ...
    async def _insert_to_weaviate(
        self,
        enriched_tuples: List[Tuple[Chunk, Dict[str, Any]]],
        embeddings_list: List[Optional[Any]],
        batch_inserter: Any,
    ) -> Tuple[int, List[Dict[str, Any]]]: ...
    async def shutdown(self) -> None: ...
    def get_stats(self) -> Dict[str, Any]: ...
