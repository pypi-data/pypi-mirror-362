"""
Indexing Worker Pool - Parallel processing for indexing service.

Manages a pool of workers for parallel file indexing.
Separate from IndexingService to maintain single responsibility.

🚨 CRITICAL BUG WORKAROUND - weaviate-client v3.26.7 Threading Issues:

IDENTIFIED PROBLEM:
- weaviate-client v3.26.7 has severe issues with multiple concurrent clients
- Causes: "ResourceWarning: unclosed transport", "This event loop is already running"
- Symptoms: Hanging tasks, memory leaks, performance degradation
- Detected in: tests/install/index/layer_3b_concurrency/test_worker_pool.py

APPLIED WORKAROUND:
- Changed from N individual clients to 1 shared client across workers
- Method: _create_weaviate_clients() uses [shared_client] * num_workers
- Status: TEMPORARY - works but not optimal for thread-safety

DEFINITIVE SOLUTION:
- Update to weaviate-client v4.x which fixes threading issues
- Reference: https://weaviate.io/developers/weaviate/client-libraries/python
- v4.x introduces proper async support and eliminates event loop conflicts

TESTS FIXED:
- test_worker_pool.py now uses shared mocked clients
- test_parallel_decision.py with appropriate mocks to avoid real clients
"""

import asyncio
from typing import List, Dict, Any, Optional, TYPE_CHECKING, Union, cast
import os

from acolyte.core.logging import logger, PerformanceLogger
from acolyte.core.tracing import MetricsCollector
from acolyte.core.secure_config import Settings
from acolyte.models.chunk import Chunk

if TYPE_CHECKING:
    from acolyte.services.indexing_service import IndexingService
    from acolyte.embeddings.unixcoder import UniXcoderEmbeddings


class IndexingWorkerPool:
    """
    Manages parallel workers for indexing operations.

    Features:
    - Configurable number of workers
    - Dedicated Weaviate client per worker (thread-safety)
    - Embeddings semaphore for GPU protection
    - Progress tracking and error collection
    """

    def __init__(
        self,
        indexing_service: 'IndexingService',
        num_workers: int = 4,
        embeddings_semaphore_size: int = 2,
    ):
        """
        Initialize the worker pool.

        Args:
            indexing_service: Parent indexing service for utilities
            num_workers: Number of parallel workers
            embeddings_semaphore_size: Max concurrent embedding operations
        """
        self.indexing_service = indexing_service
        self.num_workers = num_workers
        self.config = Settings()
        self.metrics = MetricsCollector()
        self.perf_logger = PerformanceLogger()

        # Worker components
        self._file_queue: asyncio.Queue = asyncio.Queue()
        self._worker_tasks: List[asyncio.Task] = []
        self._weaviate_clients: List[Optional[Any]] = []
        self._embeddings_semaphore = asyncio.Semaphore(embeddings_semaphore_size)

        # DEADLOCK FIX: One EnrichmentService per worker (each with its own git.Repo)
        self._enrichment_services: List[Optional[Any]] = []

        # Results tracking
        self._worker_results: Dict[int, Dict[str, Any]] = {}
        self._shutdown_event = asyncio.Event()
        self._initialized = False

        logger.info(
            "IndexingWorkerPool created",
            num_workers=num_workers,
            embeddings_semaphore=embeddings_semaphore_size,
        )

    async def initialize(self):
        """Initialize worker pool resources."""
        if self._initialized:
            return

        logger.info("Initializing worker pool")

        # Create Weaviate clients (one per worker for thread safety)
        await self._create_weaviate_clients()

        # DEADLOCK FIX: Create one EnrichmentService per worker (each with its own git.Repo)
        await self._create_enrichment_services()

        # Start worker tasks
        for i in range(self.num_workers):
            worker_task = asyncio.create_task(self._worker(i))
            self._worker_tasks.append(worker_task)

        self._initialized = True
        logger.info("Worker pool initialized", active_workers=len(self._worker_tasks))

    async def _create_weaviate_clients(self):
        """Create shared Weaviate client - WORKAROUND for v3.26.7 threading issues."""
        try:
            import weaviate
        except ImportError:
            logger.warning("Weaviate not available, workers will skip insertion")
            return

        # Obtener la URL de Weaviate respetando la variable de entorno
        weaviate_url = os.getenv(
            "WEAVIATE_URL", f"http://localhost:{self.config.get('ports.weaviate', 8080)}"
        )

        try:
            shared_client = weaviate.Client(weaviate_url)
            if shared_client.is_ready():
                # Share the same client between all workers
                self._weaviate_clients = [shared_client] * self.num_workers
                logger.info(
                    "Created shared Weaviate client for all workers - v3.26.7 workaround",
                    workers=self.num_workers,
                )
            else:
                logger.warning("Shared Weaviate client not ready")
                self._weaviate_clients = [None] * self.num_workers
        except Exception as e:
            logger.error("Failed to create shared Weaviate client", error=str(e))
            self._weaviate_clients = [None] * self.num_workers

    async def _create_enrichment_services(self):
        """Create dedicated EnrichmentService per worker - DEADLOCK FIX for git.Repo sharing."""
        try:
            from acolyte.rag.enrichment.service import EnrichmentService
        except ImportError as e:
            logger.error("Failed to import EnrichmentService", error=str(e))
            self._enrichment_services = [None] * self.num_workers
            return

        # Get project path from the main indexing service
        project_path = getattr(self.indexing_service, 'project_path', None)
        if project_path is None:
            # Fallback: try to get from enrichment service if it exists
            if hasattr(self.indexing_service, 'enrichment') and self.indexing_service.enrichment:
                project_path = str(self.indexing_service.enrichment.repo_path)
            else:
                project_path = "."  # Current directory as last resort

        try:
            # Create one EnrichmentService per worker (each with its own git.Repo)
            for i in range(self.num_workers):
                try:
                    enrichment_service = EnrichmentService(project_path)
                    self._enrichment_services.append(enrichment_service)

                    # Debug logging to verify each worker gets its own instance
                    logger.debug(
                        "Created EnrichmentService for worker",
                        worker_id=i,
                        has_git=enrichment_service.has_git,
                        repo_path=str(enrichment_service.repo_path),
                        instance_id=hex(id(enrichment_service)),
                    )
                except Exception as e:
                    logger.error("Failed to create EnrichmentService", error=str(e), worker_id=i)
                    self._enrichment_services.append(None)

            successful_services = len([e for e in self._enrichment_services if e])
            logger.info(
                "Created dedicated EnrichmentService per worker - deadlock fix",
                workers=self.num_workers,
                successful_services=successful_services,
                project_path=project_path,
            )
        except Exception as e:
            logger.error("Failed to create EnrichmentServices per worker", error=str(e))
            self._enrichment_services = [None] * self.num_workers

    async def process_files(
        self, files: List[str], batch_size: int = 10, trigger: str = "manual"
    ) -> Dict[str, Any]:
        """
        Process files using the worker pool.

        Args:
            files: List of file paths to process
            batch_size: Files per worker batch
            trigger: Indexing trigger type

        Returns:
            Aggregated results from all workers
        """
        if not self._initialized:
            await self.initialize()

        # Reset results
        self._worker_results.clear()

        # Queue file batches
        total_batches = 0
        for i in range(0, len(files), batch_size):
            batch = files[i : i + batch_size]
            await self._file_queue.put((batch, trigger))
            total_batches += 1

        logger.info(
            "Queued files for parallel processing",
            total_files=len(files),
            batches=total_batches,
            batch_size=batch_size,
        )

        # Wait for all batches to be processed with timeout
        try:
            queue_timeout = self.config.get("indexing.queue_timeout", 600.0)  # 10 minutes default
            await asyncio.wait_for(self._file_queue.join(), timeout=queue_timeout)
            logger.info("All batches processed successfully")
        except asyncio.TimeoutError:
            queue_timeout = self.config.get("indexing.queue_timeout", 600.0)
            logger.error(
                "Timeout waiting for file queue to complete",
                pending_tasks=self._file_queue.qsize(),
                worker_results=len(self._worker_results),
                total_batches=total_batches,
                timeout=queue_timeout,
            )
            # Force clear the queue if it's stuck
            while not self._file_queue.empty():
                try:
                    self._file_queue.get_nowait()
                    self._file_queue.task_done()
                except asyncio.QueueEmpty:
                    break
            logger.warning("Forced queue cleanup completed")

        # Aggregate results
        total_chunks = 0
        total_embeddings = 0
        all_errors = []

        for worker_id, result in self._worker_results.items():
            total_chunks += result.get("chunks_created", 0)
            total_embeddings += result.get("embeddings_created", 0)
            if result.get("errors"):
                all_errors.extend(result["errors"])

        return {
            "chunks_created": total_chunks,
            "embeddings_created": total_embeddings,
            "errors": all_errors,
            "workers_used": len(self._worker_results),
        }

    async def _worker(self, worker_id: int):
        """Individual worker process."""
        logger.info("Worker started", worker_id=worker_id)

        # Get dedicated Weaviate client
        weaviate_client = (
            self._weaviate_clients[worker_id] if worker_id < len(self._weaviate_clients) else None
        )

        # Create batch inserter if Weaviate available
        batch_inserter = None
        if weaviate_client:
            try:
                from acolyte.rag.collections import WeaviateBatchInserter

                batch_inserter = WeaviateBatchInserter(weaviate_client, self.config)
            except ImportError:
                logger.warning("Worker batch inserter not available", worker_id=worker_id)

        while not self._shutdown_event.is_set():
            batch_data = None
            got_item = False

            try:
                # Get work with timeout to check shutdown
                try:
                    batch_data = await asyncio.wait_for(self._file_queue.get(), timeout=1.0)
                    got_item = True
                except asyncio.TimeoutError:
                    continue

                if batch_data is None:  # Shutdown signal
                    break

                file_batch, trigger = batch_data
                logger.info(
                    "Worker processing batch", worker_id=worker_id, files_count=len(file_batch)
                )

                # Process the batch
                result = await self._process_file_batch(
                    worker_id, file_batch, trigger, batch_inserter
                )

                # Accumulate results instead of overwriting
                if worker_id not in self._worker_results:
                    self._worker_results[worker_id] = {
                        "chunks_created": 0,
                        "embeddings_created": 0,
                        "errors": [],
                        "files_processed": 0,
                    }

                # Add to existing results
                self._worker_results[worker_id]["chunks_created"] += result.get("chunks_created", 0)
                self._worker_results[worker_id]["embeddings_created"] += result.get(
                    "embeddings_created", 0
                )
                self._worker_results[worker_id]["errors"].extend(result.get("errors", []))
                self._worker_results[worker_id]["files_processed"] += result.get(
                    "files_processed", 0
                )

                # Update metrics
                self.metrics.increment(f"indexing.worker_{worker_id}.batches_processed")

                logger.info(
                    "Worker completed batch",
                    worker_id=worker_id,
                    chunks_created=result.get("chunks_created", 0),
                    embeddings_created=result.get("embeddings_created", 0),
                    errors_count=len(result.get("errors", [])),
                )

            except Exception as e:
                logger.error("Worker error", worker_id=worker_id, error=str(e), exc_info=True)
                # Store error result if we got an item
                if got_item:
                    if worker_id not in self._worker_results:
                        self._worker_results[worker_id] = {
                            "chunks_created": 0,
                            "embeddings_created": 0,
                            "errors": [],
                            "files_processed": 0,
                        }

                    # Add error to existing results
                    self._worker_results[worker_id]["errors"].append(
                        {
                            "worker_id": worker_id,
                            "error": str(e),
                            "error_type": type(e).__name__,
                        }
                    )

            finally:
                # Only call task_done() if we successfully got an item
                if got_item:
                    self._file_queue.task_done()
                    logger.debug("Worker marked task as done", worker_id=worker_id)

        logger.info("Worker stopped", worker_id=worker_id)

    async def _process_file_batch(
        self, worker_id: int, files: List[str], trigger: str, batch_inserter: Optional[Any]
    ) -> Dict[str, Any]:
        """Process a batch of files."""
        chunks_created = 0
        embeddings_created = 0
        errors = []

        try:
            with self.perf_logger.measure(f"worker_{worker_id}_batch", files_count=len(files)):
                # Step 1: Chunk files
                chunks = await self.indexing_service._chunk_files(files)
                if not chunks:
                    return {
                        "chunks_created": 0,
                        "embeddings_created": 0,
                        "errors": [],
                        "files_processed": len(files),
                    }

                # Count chunks as soon as they are created
                chunks_created = len(chunks)

                # Step 2: Enrich chunks (with timeout) - DEADLOCK FIX: use worker-specific service
                logger.debug(
                    "Starting enrichment phase",
                    worker_id=worker_id,
                    chunks_count=len(chunks),
                    files_sample=files[:3] if files else [],  # First 3 files for debug
                    trigger=trigger,
                )

                try:
                    enrichment_timeout = self.config.get(
                        "indexing.enrichment_timeout", 180.0
                    )  # 3 minutes default
                    enriched_tuples = await asyncio.wait_for(
                        self._enrich_chunks(worker_id, chunks, trigger), timeout=enrichment_timeout
                    )
                except asyncio.TimeoutError:
                    enrichment_timeout = self.config.get("indexing.enrichment_timeout", 180.0)
                    logger.warning(
                        "Enrichment timeout for worker",
                        worker_id=worker_id,
                        timeout=enrichment_timeout,
                    )
                    enriched_tuples = [
                        (chunk, {}) for chunk in chunks
                    ]  # Fallback to empty metadata

                # Step 3: Generate embeddings (with semaphore and timeout)
                try:
                    embeddings_timeout = self.config.get(
                        "indexing.embeddings_timeout", 240.0
                    )  # 4 minutes default
                    embeddings_list = await asyncio.wait_for(
                        self._generate_embeddings(worker_id, enriched_tuples),
                        timeout=embeddings_timeout,
                    )
                except asyncio.TimeoutError:
                    embeddings_timeout = self.config.get("indexing.embeddings_timeout", 240.0)
                    logger.warning(
                        "Embeddings timeout for worker",
                        worker_id=worker_id,
                        timeout=embeddings_timeout,
                    )
                    embeddings_list = [None] * len(enriched_tuples)  # Fallback to no embeddings

                embeddings_created = len([e for e in embeddings_list if e is not None])

                # Step 4: Insert to Weaviate (with timeout)
                if batch_inserter and embeddings_list:
                    try:
                        weaviate_timeout = self.config.get(
                            "indexing.weaviate_timeout", 120.0
                        )  # 2 minutes default
                        _, insert_errors = await asyncio.wait_for(
                            self._insert_to_weaviate(
                                enriched_tuples, embeddings_list, batch_inserter
                            ),
                            timeout=weaviate_timeout,
                        )
                        errors.extend(insert_errors)
                    except asyncio.TimeoutError:
                        weaviate_timeout = self.config.get("indexing.weaviate_timeout", 120.0)
                        logger.warning(
                            "Weaviate insertion timeout for worker",
                            worker_id=worker_id,
                            timeout=weaviate_timeout,
                        )
                        errors.append(
                            {
                                "worker_id": worker_id,
                                "error": "Weaviate insertion timeout after 60s",
                                "error_type": "TimeoutError",
                                "step": "weaviate_insertion",
                            }
                        )
                else:
                    # Log why insertion was skipped
                    if not batch_inserter:
                        logger.debug(
                            "Skipping Weaviate insertion - no batch inserter", worker_id=worker_id
                        )
                    elif not embeddings_list:
                        logger.debug(
                            "Skipping Weaviate insertion - no embeddings", worker_id=worker_id
                        )

        except Exception as e:
            logger.error("Worker batch failed", worker_id=worker_id, error=str(e), files=files)
            errors.append(
                {
                    "worker_id": worker_id,
                    "files": files,
                    "error": str(e),
                    "error_type": type(e).__name__,
                }
            )

        return {
            "chunks_created": chunks_created,
            "embeddings_created": embeddings_created,
            "errors": errors,
            "files_processed": len(files),
        }

    async def _enrich_chunks(
        self, worker_id: int, chunks: List[Chunk], trigger: str
    ) -> List[tuple[Chunk, Dict[str, Any]]]:
        """Enrich chunks with metadata using worker-specific EnrichmentService."""
        # DEADLOCK FIX: Use worker-specific EnrichmentService (with its own git.Repo)
        if (
            worker_id < len(self._enrichment_services)
            and self._enrichment_services[worker_id] is not None
        ):
            try:
                worker_enrichment = self._enrichment_services[worker_id]
                # Type safety: worker_enrichment is guaranteed not None by the if condition
                assert (
                    worker_enrichment is not None
                ), "EnrichmentService should not be None after check"

                # Debug logging to verify worker uses its dedicated instance
                logger.debug(
                    "Worker using dedicated EnrichmentService",
                    worker_id=worker_id,
                    enrichment_instance_id=hex(id(worker_enrichment)),
                    has_git=worker_enrichment.has_git,
                    chunks_count=len(chunks),
                )

                return await worker_enrichment.enrich_chunks(chunks, trigger=trigger)
            except Exception as e:
                logger.error(
                    "Worker enrichment failed",
                    worker_id=worker_id,
                    error=str(e),
                    chunks_count=len(chunks),
                )
                # Fallback: empty metadata on error
                return [(chunk, {}) for chunk in chunks]

        # Fallback: empty metadata if enrichment not available for this worker
        logger.debug("No enrichment service available for worker", worker_id=worker_id)
        return [(chunk, {}) for chunk in chunks]

    async def _generate_embeddings(
        self, worker_id: int, enriched_tuples: List[tuple[Chunk, Dict[str, Any]]]
    ) -> List[Optional[Any]]:
        """Generate embeddings with GPU protection."""
        if not self.indexing_service._ensure_embeddings():
            return []

        chunks_content: list[Union[str, Chunk]] = [chunk.content for chunk, _ in enriched_tuples]
        embeddings_list = []

        try:
            # Use semaphore to limit GPU concurrency
            async with self._embeddings_semaphore:
                logger.debug("Worker acquired embeddings semaphore", worker_id=worker_id)

                max_tokens = self.config.get("embeddings.max_tokens_per_batch", 10000)
                assert (
                    self.indexing_service.embeddings is not None
                ), "Embeddings service must be initialized"
                embeddings_service = cast("UniXcoderEmbeddings", self.indexing_service.embeddings)
                embeddings_list = embeddings_service.encode_batch(
                    texts=chunks_content, max_tokens_per_batch=max_tokens
                )

                logger.debug(
                    "Worker generated embeddings", worker_id=worker_id, count=len(embeddings_list)
                )

        except Exception as e:
            logger.error("Worker embeddings failed", worker_id=worker_id, error=str(e))
            # Return None for each chunk
            embeddings_list = [None] * len(chunks_content)

        return embeddings_list

    async def _insert_to_weaviate(
        self,
        enriched_tuples: List[tuple[Chunk, Dict[str, Any]]],
        embeddings_list: List[Optional[Any]],
        batch_inserter: Any,
    ) -> tuple[int, List[Dict[str, Any]]]:
        """Insert chunks to Weaviate."""
        weaviate_objects = []
        vectors_list = []

        for i, (chunk, metadata) in enumerate(enriched_tuples):
            obj = self.indexing_service._prepare_weaviate_object(chunk, metadata)
            weaviate_objects.append(obj)

            embedding = embeddings_list[i] if i < len(embeddings_list) else None
            if embedding:
                # Handle different embedding types
                from acolyte.embeddings.types import EmbeddingVector

                if isinstance(embedding, EmbeddingVector):
                    vector = embedding.to_weaviate()
                elif hasattr(embedding, "to_weaviate"):
                    vector = embedding.to_weaviate()
                else:
                    vector = list(embedding)
                vectors_list.append(vector)
            else:
                vectors_list.append(None)

        # Batch insert
        return await batch_inserter.batch_insert_with_fallback(
            data_objects=weaviate_objects, vectors=vectors_list, class_name="CodeChunk"
        )

    async def shutdown(self):
        """Gracefully shutdown the worker pool."""
        logger.info("Shutting down worker pool")

        # Signal shutdown
        self._shutdown_event.set()

        # Send shutdown signals to queue
        if self._file_queue:
            for _ in range(self.num_workers):
                await self._file_queue.put(None)

        # Wait for workers to finish with timeout
        if self._worker_tasks:
            try:
                # Give workers 5 seconds to finish gracefully
                results = await asyncio.wait_for(
                    asyncio.gather(*self._worker_tasks, return_exceptions=True), timeout=5.0
                )
                # Check results for any non-CancelledError exceptions
                for i, result in enumerate(results):
                    if isinstance(result, Exception) and not isinstance(
                        result, asyncio.CancelledError
                    ):
                        logger.warning(f"Worker {i} finished with exception", error=str(result))
                logger.info("All workers finished gracefully")
            except asyncio.TimeoutError:
                logger.warning("Workers did not finish in time, cancelling")
                # Cancel remaining tasks
                for task in self._worker_tasks:
                    if not task.done():
                        task.cancel()

                # Wait briefly for cancellations to process with proper exception handling
                try:
                    cancellation_results = await asyncio.wait_for(
                        asyncio.gather(*self._worker_tasks, return_exceptions=True), timeout=2.0
                    )
                    # Count how many were successfully cancelled
                    cancelled_count = sum(
                        1 for r in cancellation_results if isinstance(r, asyncio.CancelledError)
                    )
                    logger.info(
                        f"Successfully cancelled {cancelled_count}/{len(self._worker_tasks)} worker tasks"
                    )
                except asyncio.TimeoutError:
                    logger.warning("Some workers did not respond to cancellation within 2 seconds")
                except Exception as e:
                    logger.warning(f"Error during worker cancellation: {e}")
            except Exception as e:
                # Catch any other unexpected errors during shutdown
                logger.error(f"Unexpected error during worker pool shutdown: {e}")
                # Still try to cancel tasks
                for task in self._worker_tasks:
                    if not task.done():
                        task.cancel()

        # Cleanup
        self._worker_tasks.clear()
        self._weaviate_clients.clear()

        # Clear EnrichmentService references
        self._enrichment_services.clear()

        self._initialized = False

        logger.info("Worker pool shutdown complete")

    def get_stats(self) -> Dict[str, Any]:
        """Get worker pool statistics."""
        return {
            "num_workers": self.num_workers,
            "active_workers": len(self._worker_tasks),
            "queue_size": self._file_queue.qsize() if self._file_queue else 0,
            "results_collected": len(self._worker_results),
            "weaviate_clients": len([c for c in self._weaviate_clients if c]),
            "enrichment_services": len([e for e in self._enrichment_services if e]),
            "enrichment_services_with_git": len(
                [e for e in self._enrichment_services if e and e.has_git]
            ),
            "initialized": self._initialized,
        }
