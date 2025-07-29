"""
GraphBuilder - Updates neural graph from enriched chunks.

Extracts relationships (imports, calls, extends) from code
and updates the graph database.

CREATED: To automatically update the neural graph (/rag/graph/) during
the enrichment process. This ensures the graph stays synchronized with
code changes without manual intervention.

INTEGRATION: Called automatically by EnrichmentService.enrich_chunks()
after Git metadata extraction to build/update code relationships.
"""

from typing import List, Dict, Any, Set
import re
import ast
import asyncio

from acolyte.core.logging import logger
from acolyte.core.tracing import MetricsCollector
from acolyte.rag.graph import NeuralGraph
from acolyte.models.chunk import Chunk, ChunkType


class GraphBuilder:
    """
    Builds and updates the neural graph from code analysis.

    Called by EnrichmentService after chunks are enriched.
    """

    # Set compartido entre TODAS las instancias para trackear archivos procesados
    _processed_files: Set[str] = set()
    _flush_lock = None
    _files_lock = None

    @classmethod
    def _get_flush_lock(cls):
        """Get or create the flush lock - lazy initialization for asyncio compatibility."""
        if cls._flush_lock is None:
            cls._flush_lock = asyncio.Lock()
        return cls._flush_lock

    @classmethod
    def _get_files_lock(cls):
        """Get or create the files lock - lazy initialization for asyncio compatibility."""
        if cls._files_lock is None:
            cls._files_lock = asyncio.Lock()
        return cls._files_lock

    def __init__(self):
        self.graph = NeuralGraph()
        self.metrics = MetricsCollector()

    async def update_from_chunks(self, chunks: List[Chunk], metadata: Dict[str, Any]) -> None:
        """
        Update graph from enriched chunks.

        Args:
            chunks: List of code chunks to analyze
            metadata: Enrichment metadata (includes Git info)
        """
        logger.info(f"Updating graph from {len(chunks)} chunks")
        self.metrics.increment("rag.graph_builder.update_calls")
        self.metrics.gauge("rag.graph_builder.chunks_per_update", len(chunks))

        # OPTIMIZATION: Batch collect all nodes first
        nodes_to_create = []
        chunks_by_file = {}

        # Group chunks by file for efficient processing
        for chunk in chunks:
            file_path = chunk.metadata.file_path
            if file_path not in chunks_by_file:
                chunks_by_file[file_path] = []
            chunks_by_file[file_path].append(chunk)

        # Collect all FILE nodes to create
        async with GraphBuilder._get_files_lock():
            for file_path in chunks_by_file.keys():
                if file_path not in GraphBuilder._processed_files:
                    nodes_to_create.append(("FILE", file_path, file_path.split("/")[-1], None))
                    GraphBuilder._processed_files.add(file_path)

        # Batch create FILE nodes
        if nodes_to_create:
            try:
                await self.graph.add_nodes_batch(nodes_to_create)
                self.metrics.increment(
                    "rag.graph_builder.batch_nodes_created", len(nodes_to_create)
                )
                logger.info(f"Batch created {len(nodes_to_create)} FILE nodes")
            except Exception as e:
                logger.error(f"Failed to batch create FILE nodes: {e}")
                # Fallback handled in add_nodes_batch

        # Now process chunks for other node types
        for chunk in chunks:
            try:
                await self._process_chunk(chunk, metadata)
            except Exception as e:
                logger.error(f"Error processing chunk for graph: {chunk.metadata.file_path}: {e}")
                self.metrics.increment("rag.graph_builder.chunk_errors")
                continue

        # Update co-modification patterns if Git metadata available
        if metadata.get("git", {}).get("co_modified_with"):
            await self._update_co_modifications(set(chunks_by_file.keys()), metadata["git"])

        # Procesar todas las aristas pendientes después de crear todos los nodos
        # Usar lock de clase para evitar que múltiples instancias ejecuten flush_edges() simultáneamente
        async with GraphBuilder._get_flush_lock():
            try:
                await self.graph.flush_edges()
                logger.info("Graph edges flushed successfully")
            except Exception as e:
                logger.error(f"Error flushing edges: {e}")
                self.metrics.increment("rag.graph_builder.flush_errors")

        logger.info("Graph update completed")

    async def _process_chunk(self, chunk: Chunk, metadata: Dict[str, Any]) -> None:
        """Process a single chunk to extract relationships."""
        file_path = chunk.metadata.file_path
        logger.info(
            f"Processing chunk: file_path={file_path}, chunk_type={chunk.metadata.chunk_type}"
        )

        chunk_type = chunk.metadata.chunk_type
        if isinstance(chunk_type, ChunkType):
            chunk_type = chunk_type.value

        # FILE nodes are now created in batch in update_from_chunks
        # Just verify it exists
        if file_path not in GraphBuilder._processed_files:
            logger.warning(f"FILE node should have been created in batch for {file_path}")
            return  # Cannot continue without FILE node

        # Extract relationships based on chunk type
        logger.info(
            f"About to check chunk type: {chunk_type} == 'function'? {chunk_type == 'function'}"
        )

        if chunk_type == ChunkType.FUNCTION.value or chunk_type == ChunkType.METHOD.value:
            logger.info("Processing as function")
            await self._process_function(chunk, file_path)
        elif chunk_type == ChunkType.CLASS.value:
            await self._process_class(chunk, file_path)
        elif chunk_type == ChunkType.MODULE.value:
            await self._process_module(chunk, file_path)
        elif chunk_type == ChunkType.IMPORTS.value:
            await self._process_imports(chunk, file_path)
        else:
            logger.info(f"Chunk type {chunk_type} not handled")

    async def _process_function(self, chunk: Chunk, file_path: str) -> None:
        """Extract function relationships."""
        logger.info(f"_process_function called for {file_path}")
        func_name = chunk.metadata.name or "unknown_function"
        func_path = f"{file_path}::{func_name}"
        logger.info(f"About to add FUNCTION node: {func_path}")

        # Add function node first
        try:
            func_node_id = await self.graph.add_node("FUNCTION", func_path, func_name)
            if func_node_id:
                self.metrics.increment("rag.graph_builder.nodes_created")
                logger.debug(f"Successfully created FUNCTION node for {func_path}")
            else:
                logger.error(
                    f"Failed to create FUNCTION node for {func_path} - add_node returned None"
                )
                return  # Cannot continue without FUNCTION node
        except Exception as e:
            logger.error(f"Failed to create FUNCTION node for {func_path}: {e}")
            return  # Cannot continue without FUNCTION node

        # Add USES relationship (file uses function) - only if both nodes exist
        try:
            await self.graph.add_edge_deferred(file_path, func_path, "USES")
            self.metrics.increment("rag.graph_builder.edges_created")
            logger.debug(f"Successfully deferred USES edge: {file_path} -> {func_path}")
        except Exception as e:
            logger.warning(f"Could not defer USES edge {file_path} -> {func_path}: {e}")
            # Continue even if edge creation fails

        # Extract function calls using simple pattern matching
        # (More sophisticated AST parsing would be better but requires language detection)
        call_pattern = r'(\w+)\s*\('
        calls = re.findall(call_pattern, chunk.content)

        for called_func in set(calls):
            if called_func not in ['if', 'for', 'while', 'return', 'print']:  # Skip keywords
                called_path = f"unknown::{called_func}"
                try:
                    # Create unknown node first to avoid NotFoundError
                    called_node_id = await self.graph.add_node(
                        "FUNCTION",
                        called_path,
                        called_func,
                        metadata={"inferred": True, "incomplete": True, "source": "function_call"},
                    )
                    if called_node_id:
                        # Only create edge if called node was created successfully
                        try:
                            await self.graph.add_edge_deferred(func_path, called_path, "CALLS")
                            logger.debug(
                                f"Successfully deferred CALLS edge: {func_path} -> {called_path}"
                            )
                        except Exception as e:
                            logger.warning(
                                f"Could not defer CALLS edge {func_path} -> {called_path}: {e}"
                            )
                    else:
                        logger.warning(
                            f"Failed to create called FUNCTION node for {called_path} - skipping call edge"
                        )
                except Exception as e:
                    logger.warning(f"Failed to create called FUNCTION node for {called_path}: {e}")
                    continue

    async def _process_class(self, chunk: Chunk, file_path: str) -> None:
        """Extract class relationships."""
        class_name = chunk.metadata.name or "unknown_class"
        class_path = f"{file_path}::{class_name}"

        # Add class node first
        try:
            class_node_id = await self.graph.add_node("CLASS", class_path, class_name)
            if class_node_id:
                self.metrics.increment("rag.graph_builder.nodes_created")
                logger.debug(f"Successfully created CLASS node for {class_path}")
            else:
                logger.error(
                    f"Failed to create CLASS node for {class_path} - add_node returned None"
                )
                return  # Cannot continue without CLASS node
        except Exception as e:
            logger.error(f"Failed to create CLASS node for {class_path}: {e}")
            return  # Cannot continue without CLASS node

        # Add USES relationship (file uses class) - only if both nodes exist
        try:
            await self.graph.add_edge_deferred(file_path, class_path, "USES")
            self.metrics.increment("rag.graph_builder.edges_created")
            logger.debug(f"Successfully deferred USES edge: {file_path} -> {class_path}")
        except Exception as e:
            logger.warning(f"Could not defer USES edge {file_path} -> {class_path}: {e}")
            # Continue even if edge creation fails

        # Try to extract inheritance (simple pattern)
        inherit_pattern = r'class\s+\w+\s*\(([^)]+)\)'
        match = re.search(inherit_pattern, chunk.content)

        if match:
            parents = match.group(1).split(',')
            for parent in parents:
                parent_name = parent.strip()
                if parent_name and parent_name != 'object':
                    parent_path = f"unknown::{parent_name}"
                    # Create unknown parent class node first
                    try:
                        parent_node_id = await self.graph.add_node(
                            "CLASS",
                            parent_path,
                            parent_name,
                            metadata={
                                "inferred": True,
                                "incomplete": True,
                                "source": "inheritance",
                            },
                        )
                        if parent_node_id:
                            # Only create edge if parent node was created successfully
                            try:
                                await self.graph.add_edge_deferred(
                                    class_path, parent_path, "EXTENDS"
                                )
                                logger.debug(
                                    f"Successfully deferred EXTENDS edge: {class_path} -> {parent_path}"
                                )
                            except Exception as e:
                                logger.warning(
                                    f"Could not defer EXTENDS edge {class_path} -> {parent_path}: {e}"
                                )
                        else:
                            logger.warning(
                                f"Failed to create parent CLASS node for {parent_path} - skipping inheritance edge"
                            )
                    except Exception as e:
                        logger.warning(f"Failed to create parent CLASS node for {parent_path}: {e}")
                        continue

    async def _process_module(self, chunk: Chunk, file_path: str) -> None:
        """Process module-level code."""
        # For Python, extract imports
        await self._process_imports(chunk, file_path)

    async def _process_imports(self, chunk: Chunk, file_path: str) -> None:
        """Extract import relationships."""
        content = chunk.content

        # Python imports
        import_patterns = [r'from\s+([\w.]+)\s+import', r'import\s+([\w.]+)']

        for pattern in import_patterns:
            imports = re.findall(pattern, content)
            for module in imports:
                # Convert module to approximate file path
                module_path = module.replace('.', '/')
                if not module_path.endswith('.py'):
                    module_path += '.py'

                # Create module node if it doesn't exist
                try:
                    module_node_id = await self.graph.add_node(
                        "MODULE",
                        module_path,
                        module,
                        metadata={"inferred": True, "from_import": True},
                    )
                    if module_node_id:
                        # Only create edge if module node was created successfully
                        try:
                            await self.graph.add_edge_deferred(
                                file_path,
                                module_path,
                                "IMPORTS",
                                metadata={"import_type": "python"},
                            )
                            logger.debug(
                                f"Successfully deferred IMPORTS edge: {file_path} -> {module_path}"
                            )
                        except Exception as e:
                            logger.warning(
                                f"Could not defer IMPORTS edge {file_path} -> {module_path}: {e}"
                            )
                    else:
                        logger.warning(
                            f"Failed to create MODULE node for {module_path} - skipping import edge"
                        )
                except Exception as e:
                    logger.warning(f"Failed to create MODULE node for {module_path}: {e}")
                    continue

    async def _update_co_modifications(
        self, files_in_batch: Set[str], git_metadata: Dict[str, Any]
    ) -> None:
        """Update co-modification relationships from Git data."""
        co_modified = git_metadata.get("co_modified_with", [])

        for file_path in files_in_batch:
            for co_file in co_modified:
                if co_file != file_path:
                    # Add or strengthen co-modification edge
                    try:
                        await self.graph.add_edge_deferred(
                            file_path, co_file, "MODIFIES_TOGETHER", discovered_by="GIT_ACTIVITY"
                        )
                        logger.debug(
                            f"Successfully deferred MODIFIES_TOGETHER edge: {file_path} -> {co_file}"
                        )
                    except Exception as e:
                        logger.warning(
                            f"Could not defer MODIFIES_TOGETHER edge {file_path} -> {co_file}: {e}"
                        )
                        continue

    async def extract_relationships_from_ast(
        self, chunk: Chunk, language: str = "python"
    ) -> Dict[str, List[str]]:
        """
        Extract relationships using AST parsing (more accurate).

        Currently only supports Python. Other languages would need
        their own parsers.

        WARNING: This method only extracts relationship names. If you use
        these to create edges, ensure target nodes exist first or create
        them as 'unknown' nodes to avoid NotFoundError.
        """
        if language != "python":
            return {}

        try:
            tree = ast.parse(chunk.content)
            relationships: Dict[str, List[str]] = {"imports": [], "calls": [], "extends": []}

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        relationships["imports"].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        relationships["imports"].append(node.module)

                elif isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            relationships["extends"].append(base.id)

                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        relationships["calls"].append(node.func.id)

            return relationships

        except SyntaxError:
            # [TRACE] SyntaxError when parsing AST - line 196, 222-224 not covered
            logger.debug("Could not parse chunk as Python AST")
            return {}
