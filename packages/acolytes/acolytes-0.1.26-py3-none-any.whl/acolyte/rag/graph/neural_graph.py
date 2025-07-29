"""
Neural Graph - Code relationship graph.

Manages nodes (files, functions, classes) and their connections
(imports, calls, extends) stored in SQLite.
"""

from typing import Dict, Any, List, Optional, cast
import json

from acolyte.core.database import get_db_manager, FetchType
from acolyte.core.logging import logger
from acolyte.core.tracing import MetricsCollector
from acolyte.core.exceptions import DatabaseError, NotFoundError


class NeuralGraph:
    """
    Main neural graph class.

    Maintains structural relationships between code in SQLite.
    """

    def __init__(self):
        """Initialize graph with database connection."""
        self.db = get_db_manager()
        self.metrics = MetricsCollector()
        self._pending_edges = []  # Lista de aristas pendientes para procesar después

    async def add_node(
        self, node_type: str, path: str, name: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add or update a node in the graph.

        Args:
            node_type: FILE, FUNCTION, CLASS, MODULE
            path: Full path or path::function_name
            name: Element name
            metadata: Additional info (line, commit, etc.)

        Returns:
            Node ID
        """
        # Prepare metadata
        node_metadata = metadata or {}

        try:
            # ATOMIC SOLUTION: Use RETURNING to get ID in single query
            # This eliminates the race condition completely - no more INSERT+SELECT
            result = await self.db.execute_async(
                """
                INSERT INTO code_graph_nodes (node_type, path, name, metadata, last_seen)
                VALUES (?, ?, ?, ?, datetime('now'))
                ON CONFLICT (node_type, path) DO UPDATE SET
                    name = excluded.name,
                    metadata = excluded.metadata,
                    last_seen = datetime('now')
                RETURNING id
                """,
                (node_type, path, name, json.dumps(node_metadata)),
                FetchType.ONE,
            )

            if result.data:
                row = cast(Dict[str, Any], result.data)
                node_id = row["id"]
                self.metrics.increment("rag.graph.nodes_created")
                logger.debug(f"Added node: {node_type} {path} -> {node_id}")
                return node_id
            else:
                raise DatabaseError("RETURNING clause failed to return node ID")

        except Exception as e:
            self.metrics.increment("rag.graph.nodes_errors")
            logger.error(f"Error adding node: {e}")
            raise

    async def add_nodes_batch(
        self, nodes: List[tuple[str, str, str, Optional[Dict[str, Any]]]]
    ) -> List[str]:
        """
        Add multiple nodes in a single batch operation.

        Args:
            nodes: List of (node_type, path, name, metadata) tuples

        Returns:
            List of node IDs in the same order as input

        Performance:
            - Single transaction for all nodes
            - Much faster than individual add_node calls
        """
        if not nodes:
            return []

        node_ids = []

        # Use transaction for batch insert
        conn = self.db._get_connection()
        cursor = conn.cursor()

        try:
            # Check if we're already in a transaction
            in_transaction = conn.in_transaction

            # Only start transaction if not already in one
            if not in_transaction:
                cursor.execute("BEGIN IMMEDIATE")

            for node_type, path, name, metadata in nodes:
                node_metadata = metadata or {}
                cursor.execute(
                    """
                    INSERT INTO code_graph_nodes (node_type, path, name, metadata, last_seen)
                    VALUES (?, ?, ?, ?, datetime('now'))
                    ON CONFLICT (node_type, path) DO UPDATE SET
                        name = excluded.name,
                        metadata = excluded.metadata,
                        last_seen = datetime('now')
                    RETURNING id
                    """,
                    (node_type, path, name, json.dumps(node_metadata)),
                )

                result = cursor.fetchone()
                if result:
                    node_ids.append(result["id"])
                else:
                    # Rollback only if we started the transaction
                    if not in_transaction:
                        conn.rollback()
                    raise DatabaseError(f"Failed to insert node: {path}")

            # Commit only if we started the transaction
            if not in_transaction:
                conn.commit()

            self.metrics.increment("rag.graph.nodes_created", len(node_ids))
            logger.debug(
                f"Batch added {len(node_ids)} nodes {'in existing transaction' if in_transaction else 'in new transaction'}"
            )

            return node_ids

        except Exception as e:
            # Rollback only if we started the transaction
            if not in_transaction:
                conn.rollback()

            # If it's a transaction error, always fallback
            if "transaction" in str(e).lower():
                logger.warning(f"Transaction issue detected: {e}")
            else:
                logger.error(f"Error in batch node creation: {e}")

            self.metrics.increment("rag.graph.nodes_errors", len(nodes))
            # Fallback to individual inserts
            logger.warning("Falling back to individual node inserts")
            node_ids = []
            for node_data in nodes:
                try:
                    node_id = await self.add_node(*node_data)
                    node_ids.append(node_id)
                except Exception as individual_error:
                    logger.error(f"Failed to add node {node_data[1]}: {individual_error}")
                    node_ids.append(None)  # Placeholder for failed node
            return node_ids
        finally:
            cursor.close()

    async def add_edge_deferred(
        self,
        source: str,
        target: str,
        relation: str,
        discovered_by: str = "STATIC_ANALYSIS",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Añade arista para procesar después cuando todos los nodos existan.

        Este método implementa el patrón "deferred execution" para evitar
        race conditions durante la construcción del grafo. Las aristas se
        almacenan en memoria y se procesan en lote con flush_edges().

        Args:
            source: Source node ID or path
            target: Target node ID or path
            relation: IMPORTS, CALLS, EXTENDS, IMPLEMENTS, USES, MODIFIES_TOGETHER, BUG_PATTERN
            discovered_by: GIT_ACTIVITY, DREAM_ANALYSIS, USER_ACTIVITY, STATIC_ANALYSIS
            metadata: Additional info (line, commit, etc.)

        Performance:
            - O(1) - Solo añade a lista en memoria
            - No acceso a BD hasta flush_edges()

        Pattern:
            - Deferred Execution Pattern
            - Usado por GraphBuilder para evitar retries
        """
        self._pending_edges.append((source, target, relation, discovered_by, metadata))
        self.metrics.increment("graph.edges.deferred")

    async def flush_edges(self) -> None:
        """
        Procesa todas las aristas pendientes después de crear todos los nodos.

        RACE CONDITION FIX: Implementa reintentos, timeouts y mejor sincronización
        para resolver el problema de 62 aristas perdidas durante procesamiento paralelo.

        Performance:
            - O(n) donde n = número de aristas pendientes
            - Reutiliza lógica existente de add_edge()
            - Reintentos automáticos para fallos temporales

        Error Handling:
            - Maneja errores individualmente sin afectar el lote completo
            - Reintentos para race conditions y timeouts
            - Limpia la lista al final independientemente

        Metrics:
            - Reutiliza métricas de add_edge()
            - Tracks retries y fallos finales
        """
        edge_count = len(self._pending_edges)
        if edge_count == 0:
            return

        logger.info(f"Processing {edge_count} deferred edges")

        errors = 0
        successful = 0
        failed_edges = []  # Para reintentos

        # Primera pasada: procesamiento normal
        for edge_data in self._pending_edges:
            source, target, relation, discovered_by, metadata = edge_data
            try:
                await self.add_edge(source, target, relation, discovered_by, metadata)
                successful += 1
            except Exception as e:
                error_msg = str(e).lower()
                # Reintentar solo para race conditions y timeouts específicos
                if any(
                    keyword in error_msg for keyword in ['timeout', 'lock', 'busy', 'concurrent']
                ):
                    failed_edges.append(edge_data)
                    logger.debug(f"Deferring retry for edge {source} -> {target}: {e}")
                else:
                    logger.warning(f"Failed to create deferred edge {source} -> {target}: {e}")
                    errors += 1
                continue

        # Segunda pasada: reintentos para race conditions
        retry_errors = 0
        retry_successful = 0

        if failed_edges:
            logger.info(f"Retrying {len(failed_edges)} failed edges (race condition recovery)")
            import asyncio

            for edge_data in failed_edges:
                source, target, relation, discovered_by, metadata = edge_data
                try:
                    # Pequeño delay para evitar race condition
                    await asyncio.sleep(0.01)
                    await self.add_edge(source, target, relation, discovered_by, metadata)
                    retry_successful += 1
                except Exception as e:
                    logger.warning(f"Retry failed for deferred edge {source} -> {target}: {e}")
                    retry_errors += 1
                    continue

        # Actualizar contadores finales
        successful += retry_successful
        errors += retry_errors

        # Limpiar la lista al final
        self._pending_edges.clear()

        # Log detallado del resultado
        if retry_successful > 0 or retry_errors > 0:
            logger.info(
                f"Deferred edges processed: {successful} successful, {errors} errors "
                f"(recovered {retry_successful} from race conditions)"
            )
        else:
            logger.info(f"Deferred edges processed: {successful} successful, {errors} errors")

        # Métricas adicionales
        if errors > 0:
            self.metrics.increment("graph.edges.flush_errors", errors)
        if retry_successful > 0:
            self.metrics.increment("graph.edges.retry_recovered", retry_successful)
        self.metrics.increment("graph.edges.flushed", successful)

    async def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        discovered_by: str = "STATIC_ANALYSIS",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add or strengthen a relationship between nodes.

        Args:
            source: Source node ID or path
            target: Target node ID or path
            relation: IMPORTS, CALLS, EXTENDS, IMPLEMENTS, USES, MODIFIES_TOGETHER, BUG_PATTERN
            discovered_by: GIT_ACTIVITY, DREAM_ANALYSIS, USER_ACTIVITY, STATIC_ANALYSIS
            metadata: Additional info (line, commit, etc.)
        """
        # Resolve IDs if they are paths
        source_id = await self._resolve_node_id(source)
        target_id = await self._resolve_node_id(target)

        # Validate that both nodes exist
        if not source_id:
            raise NotFoundError(f"Node not found: {source}")
        if not target_id:
            raise NotFoundError(f"Node not found: {target}")

        # Prepare metadata
        edge_metadata = metadata or {}

        try:
            # Use the correct schema: code_graph_edges with UPSERT logic
            await self.db.execute_async(
                """
                INSERT INTO code_graph_edges 
                (source_id, target_id, relation_type, strength, discovered_by, metadata, last_reinforced)
                VALUES (?, ?, ?, 0.5, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(source_id, target_id, relation_type) DO UPDATE SET
                    strength = MIN(1.0, strength + 0.1),
                    last_reinforced = CURRENT_TIMESTAMP,
                    metadata = excluded.metadata
                """,
                (source_id, target_id, relation, discovered_by, json.dumps(edge_metadata)),
            )

            logger.debug(f"Added/strengthened edge: {source} -> {target} ({relation})")
            self.metrics.increment("rag.graph.edges_created")

        except NotFoundError:
            # Re-raise NotFoundError as-is
            raise
        except Exception as e:
            logger.error(f"Error adding edge: {e}")
            raise DatabaseError(f"Could not add edge: {e}")

    async def strengthen_edge(
        self, source: str, target: str, relation: str, delta: float = 0.1
    ) -> None:
        """
        Strengthen an existing connection.

        Args:
            source: Source ID or path
            target: Target ID or path
            relation: Relationship type
            delta: Strength increment (default 0.1)
        """
        source_id = await self._resolve_node_id(source)
        target_id = await self._resolve_node_id(target)

        if not source_id or not target_id:
            raise NotFoundError(f"Node not found: {source} or {target}")

        try:
            await self.db.execute_async(
                """
                UPDATE code_graph_edges 
                SET strength = MIN(1.0, strength + ?),
                    last_reinforced = CURRENT_TIMESTAMP
                WHERE source_id = ? AND target_id = ? AND relation_type = ?
                """,
                (delta, source_id, target_id, relation),
            )

            self.metrics.increment("graph.edges.strengthened")

        except Exception as e:
            logger.error("Error strengthening edge", error=str(e))
            raise DatabaseError(f"Could not strengthen edge: {e}")

    async def find_related(
        self, node: str, max_distance: int = 2, min_strength: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Find related nodes up to a certain distance.

        Args:
            node: Source node ID or path
            max_distance: Maximum hops (default 2)
            min_strength: Minimum connection strength

        Returns:
            List of related nodes with connection info
        """
        node_id = await self._resolve_node_id(node)
        if not node_id:
            logger.warning("[TRACE] Node not found in find_related")
            raise NotFoundError(f"Node not found: {node}")

        # BFS implementation for recursive search
        visited = {node_id}
        current_level = [
            (node_id, None, None, 1.0)
        ]  # (id, relation_type, from_node, accumulated_strength)
        all_results = []

        for distance in range(1, max_distance + 1):
            next_level = []

            # Process all nodes at current distance
            for current_id, prev_relation, prev_node, prev_strength in current_level:
                try:
                    # Find neighbors of current node
                    result = await self.db.execute_async(
                        """
                        SELECT 
                            n.id, n.node_type, n.path, n.name,
                            e.relation_type, e.strength,
                            CASE 
                                WHEN e.source_id = ? THEN 'outgoing'
                                ELSE 'incoming'
                            END as direction
                        FROM code_graph_edges e
                        JOIN code_graph_nodes n ON (
                            CASE 
                                WHEN e.source_id = ? THEN e.target_id = n.id
                                WHEN e.target_id = ? THEN e.source_id = n.id
                            END
                        )
                        WHERE e.strength >= ?
                        """,
                        (current_id, current_id, current_id, min_strength),
                        FetchType.ALL,
                    )
                    results: List[Dict[str, Any]] = result.data or []  # type: ignore

                    for row in results:
                        neighbor_id = row["id"]
                        if neighbor_id in visited:
                            continue
                        visited.add(neighbor_id)
                        strength_val = float(row["strength"])
                        accumulated_strength = prev_strength * strength_val
                        if accumulated_strength >= min_strength:
                            result_dict = dict(row)
                            result_dict["distance"] = distance
                            result_dict["accumulated_strength"] = accumulated_strength
                            result_dict["path_from_origin"] = (
                                f"{prev_node or node} -> {row['path']}"
                                if prev_node
                                else row['path']
                            )
                            all_results.append(result_dict)
                            if distance < max_distance:
                                next_level.append(
                                    (
                                        neighbor_id,
                                        row["relation_type"],
                                        row["path"],
                                        accumulated_strength,
                                    )
                                )

                except Exception as e:
                    logger.error("Error in BFS at distance", distance=distance, error=str(e))
                    continue

            # Move to next distance level
            current_level = next_level

            # Stop if no more nodes to explore
            if not current_level:
                break

        # Sort by accumulated strength (best connections first)
        all_results.sort(key=lambda x: x["accumulated_strength"], reverse=True)

        return all_results

    async def predict_impact(self, changed_node: str) -> Dict[str, Any]:
        """
        Predict the impact of changing a node.

        Args:
            changed_node: Modified node ID or path

        Returns:
            Dictionary with affected files and impact level
        """
        node_id = await self._resolve_node_id(changed_node)
        if not node_id:
            logger.warning("[TRACE] Node not found in predict_impact")
            raise NotFoundError(f"Node not found: {changed_node}")

        try:
            # Find all nodes that depend on this node
            result = await self.db.execute_async(
                """
                SELECT 
                    n.path, n.name, e.relation_type, e.strength
                FROM code_graph_edges e
                JOIN code_graph_nodes n ON e.source_id = n.id
                WHERE e.target_id = ? 
                AND e.relation_type IN ('IMPORTS', 'CALLS', 'EXTENDS', 'IMPLEMENTS', 'USES')
                ORDER BY e.strength DESC
                """,
                (node_id,),
                FetchType.ALL,
            )
            dependents: List[Dict[str, Any]] = result.data or []  # type: ignore

            # Calculate impact
            high_impact = []
            medium_impact = []
            low_impact = []

            for dep in dependents:
                strength_val = float(dep["strength"])
                if strength_val > 0.7:
                    high_impact.append(dep["path"])
                elif strength_val > 0.4:
                    medium_impact.append(dep["path"])
                else:
                    low_impact.append(dep["path"])

            return {
                "total_affected": len(dependents),
                "high_impact": high_impact,
                "medium_impact": medium_impact,
                "low_impact": low_impact,
                "details": [dict(dep) for dep in dependents],
            }

        except Exception as e:
            logger.error("Error predicting impact", error=str(e))
            raise DatabaseError(f"Could not predict impact: {e}")

    async def _resolve_node_id(self, node_ref: str) -> Optional[str]:
        """
        Resolve an ID from path or ID.

        Args:
            node_ref: Hexadecimal ID or node path

        Returns:
            Node ID or None if it doesn't exist
        """
        # If it looks like a 32-char hex ID, verify it exists
        if len(node_ref) == 32 and all(c in "0123456789abcdef" for c in node_ref):
            result = await self.db.execute_async(
                "SELECT id FROM code_graph_nodes WHERE id = ?", (node_ref,), FetchType.ONE
            )
            data: Optional[Dict[str, Any]] = result.data  # type: ignore
            return data["id"] if data else None

        # Otherwise, search by path - necesitamos node_type también para ser preciso
        # Pero como solo tenemos path, buscamos cualquier node_type con ese path
        result = await self.db.execute_async(
            "SELECT id FROM code_graph_nodes WHERE path = ? LIMIT 1", (node_ref,), FetchType.ONE
        )
        data: Optional[Dict[str, Any]] = result.data  # type: ignore
        return data["id"] if data else None
