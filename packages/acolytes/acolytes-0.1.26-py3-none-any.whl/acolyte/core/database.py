"""
Sistema de persistencia SQLite para ACOLYTE.

ESTRUCTURA DEL MÓDULO:
======================
- DatabaseManager: Infraestructura de conexión y transacciones (usado por Services)
- InsightStore: Store especializado para Dream insights (¡CORRECTAMENTE EN CORE!)

NOTA ARQUITECTÓNICA:
- Core provee infraestructura que otros módulos usan
- Services implementa la lógica de negocio usando esta infraestructura
- InsightStore es infraestructura especializada, NO lógica de negocio
"""

import os
import sqlite3
import asyncio
import threading
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
import zlib

from acolyte.core.exceptions import (
    DatabaseError,
    SQLiteBusyError,
    SQLiteCorruptError,
    SQLiteConstraintError,
)
from acolyte.core.id_generator import generate_id
from acolyte.core.logging import logger
from acolyte.core.utils.retry import retry_async, retry_sync


def _classify_sqlite_error(sqlite_error: sqlite3.Error) -> DatabaseError:
    """
    Classify SQLite specific errors and return appropriate exception.

    SQLite error types and handling:
    - SQLITE_BUSY (5): DB temporarily locked → SQLiteBusyError (RETRYABLE)
    - SQLITE_CORRUPT (11): DB corrupt → SQLiteCorruptError (NOT RETRYABLE)
    - SQLITE_CONSTRAINT (19): Constraint violation → SQLiteConstraintError (NOT RETRYABLE)
    - Others: Generic DB error → DatabaseError (RETRYABLE by default)

    Args:
        sqlite_error: Original sqlite3 error

    Returns:
        Appropriate DatabaseError instance based on type
    """
    error_msg = str(sqlite_error)
    error_code = getattr(sqlite_error, 'sqlite_errorcode', None)

    # Map SQLite codes to specific exceptions
    if error_code == 5 or 'database is locked' in error_msg.lower() or 'busy' in error_msg.lower():
        # SQLITE_BUSY: DB locked (common in concurrent writes)
        exc = SQLiteBusyError(
            f"Database temporarily locked: {error_msg}",
            context={"sqlite_code": error_code, "original_error": error_msg},
        )
        exc.add_suggestion("Retry automatically with exponential backoff")
        exc.add_suggestion("Check for long open transactions")
        return exc

    elif error_code == 11 or 'corrupt' in error_msg.lower():
        # SQLITE_CORRUPT: DB corrupt (requires manual intervention)
        exc = SQLiteCorruptError(
            f"Database corruption detected: {error_msg}",
            context={"sqlite_code": error_code, "original_error": error_msg},
        )
        exc.add_suggestion("Restore from most recent backup")
        exc.add_suggestion("Run 'PRAGMA integrity_check' for diagnostics")
        exc.add_suggestion("Consider reinitializing the database")
        return exc

    elif error_code == 19 or any(
        constraint in error_msg.lower()
        for constraint in ['unique', 'foreign key', 'check', 'not null']
    ):
        # SQLITE_CONSTRAINT: Constraint violation (logic error)
        exc = SQLiteConstraintError(
            f"Database constraint violation: {error_msg}",
            context={"sqlite_code": error_code, "original_error": error_msg},
        )
        exc.add_suggestion("Verify that data meets constraints")
        exc.add_suggestion("Review query logic or inserted values")
        return exc

    else:
        # Generic SQLite error (retryable by default)
        exc = DatabaseError(
            f"SQLite error: {error_msg}",
            context={"sqlite_code": error_code, "original_error": error_msg},
        )
        exc.add_suggestion("Verify database configuration")
        exc.add_suggestion("Check file and directory permissions")
        return exc


class FetchType(Enum):
    """Tipos de fetch para queries."""

    ONE = "one"
    ALL = "all"
    NONE = "none"


@dataclass
class QueryResult:
    """Resultado de una query."""

    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]
    rows_affected: int
    last_row_id: Optional[int]


@dataclass
class StoreResult:
    """Resultado de operación de almacenamiento."""

    success: bool
    id: str
    message: str
    stats: Dict[str, Any]


class DatabaseManager:
    """
    Gestor centralizado de base de datos SQLite.

    Características:
    1. Conexión simple para mono-usuario
    2. Transacciones ACID
    3. Optimización de índices
    4. Migración automática de esquema

    NOTA: Los esquemas SQL están definidos en database/schemas.sql
    - Usa IDs como generate_id() para compatibilidad
    - session_id es UNIQUE para integridad referencial
    - Tipos enum en MAYÚSCULAS (Python debe usar .upper())

    SEPARACIÓN DE RESPONSABILIDADES:
    ================================
    Core (este módulo) proporciona:
    - Infraestructura de conexión a BD
    - Gestión de transacciones
    - InsightStore para tabla dream_insights (usado por Dream Service)

    Services (/services) implementa:
    - ConversationService: Maneja tabla conversations
    - TaskService: Maneja tablas tasks, task_sessions, technical_decisions
    - GitService: Operaciones Git (no usa BD directamente)
    - IndexingService: Coordina indexación (usa Weaviate)

    Esta separación sigue el principio arquitectónico:
    - Core = Infraestructura base
    - Services = Lógica de negocio y gestión de datos
    """

    def __init__(self, db_path: Optional[str] = None):
        logger.info("DatabaseManager initializing...")
        try:
            self.db_path = db_path or self._get_default_path()
            self._connection = None
            self._lock = None  # Will be created lazily in the correct event loop
            self._closed = False  # Track if database has been closed

            # 🔧 CRITICAL FIX: Limpiar archivos huérfanos SQLite ANTES de crear esquema
            # Esto previene "unable to open database file" causado por archivos WAL/SHM huérfanos
            # Solución automática sin dependencias circulares
            self._cleanup_sqlite_artifacts()

            self._init_schema()
            logger.info("DatabaseManager ready", db_path=self.db_path)
        except Exception as e:
            logger.error("DatabaseManager initialization failed", error=str(e))
            raise

    def _get_default_path(self) -> str:
        """Get default database path.

        PRIORITY ORDER (FIXED FOR CONTAINERS):
        1. DATA_DIR environment (Docker containers) - HIGHEST PRIORITY
        2. .acolyte.project (configured projects) - for local development
        3. ./data/ (fallback for development)

        This ensures containers always use their mounted volumes correctly.
        """
        # Debugging: Log current working directory and environment
        cwd = Path.cwd()
        data_dir_env = os.getenv("DATA_DIR")
        logger.info(f"[DB PATH DEBUG] Current working directory: {cwd}")
        logger.info(f"[DB PATH DEBUG] DATA_DIR environment: {data_dir_env}")

        # PRIORITY 1: DATA_DIR environment variable (for Docker containers)
        # This MUST come first to avoid Path.home() issues in containers
        if data_dir_env:
            data_dir = Path(data_dir_env)
            data_dir.mkdir(exist_ok=True)
            final_path = str(data_dir / "acolyte.db")
            logger.info(f"[DB PATH DEBUG] Using DATA_DIR (priority 1): {final_path}")
            logger.info(f"[DB PATH DEBUG] Path exists: {Path(final_path).exists()}")
            return final_path

        # PRIORITY 2: Check if we're in a configured project (local development)
        project_file = Path.cwd() / ".acolyte.project"
        logger.info(f"[DB PATH DEBUG] Checking for project file: {project_file}")
        logger.info(f"[DB PATH DEBUG] Project file exists: {project_file.exists()}")

        if project_file.exists():
            try:
                import yaml

                with open(project_file) as f:
                    project_data = yaml.safe_load(f)
                    project_id = project_data.get("project_id")

                logger.info(f"[DB PATH DEBUG] Project ID found: {project_id}")
                if project_id:
                    # Use global project directory
                    global_data_dir = Path.home() / ".acolyte" / "projects" / project_id / "data"
                    global_data_dir.mkdir(parents=True, exist_ok=True)
                    final_path = str(global_data_dir / "acolyte.db")
                    logger.info(f"[DB PATH DEBUG] Using project path (priority 2): {final_path}")
                    return final_path
            except Exception as e:
                logger.warning("Failed to read project file, using local data", error=str(e))

        # PRIORITY 3: Fallback for development
        data_dir = Path("./data")
        data_dir.mkdir(exist_ok=True)
        final_path = str(data_dir / "acolyte.db")
        logger.info(f"[DB PATH DEBUG] Using fallback (priority 3): {final_path}")
        logger.info(f"[DB PATH DEBUG] Path exists: {Path(final_path).exists()}")
        return final_path

    def _cleanup_sqlite_artifacts(self):
        """
        Limpia archivos SQLite huérfanos al inicializar DatabaseManager.

        Esta función elimina archivos WAL/SHM huérfanos que pueden causar
        "unable to open database file" cuando se crea una nueva instancia
        del DatabaseManager después de que el singleton fue reseteado.

        Es segura porque:
        - Solo elimina archivos WAL vacíos (0 bytes)
        - Siempre elimina archivos SHM (seguros de eliminar)
        - No usa get_db_manager() para evitar dependencias circulares
        """
        try:
            db_path = Path(self.db_path)

            # Archivos WAL y SHM relacionados
            wal_file = db_path.with_suffix('.db-wal')
            shm_file = db_path.with_suffix('.db-shm')

            cleaned_files = []

            # Limpiar archivo WAL solo si está vacío
            if wal_file.exists():
                try:
                    # Solo eliminar WAL si está vacío para evitar pérdida de datos
                    if wal_file.stat().st_size == 0:
                        wal_file.unlink()
                        cleaned_files.append(str(wal_file.name))
                        logger.debug("Cleaned orphaned WAL file", file=str(wal_file))
                    else:
                        logger.debug(
                            "WAL file not empty, keeping it",
                            file=str(wal_file),
                            size=wal_file.stat().st_size,
                        )
                except Exception as e:
                    logger.warning("Error cleaning WAL file", file=str(wal_file), error=str(e))

            # Limpiar archivo SHM (siempre seguro)
            if shm_file.exists():
                try:
                    shm_file.unlink()
                    cleaned_files.append(str(shm_file.name))
                    logger.debug("Cleaned orphaned SHM file", file=str(shm_file))
                except Exception as e:
                    logger.warning("Error cleaning SHM file", file=str(shm_file), error=str(e))

            if cleaned_files:
                logger.info("Cleaned orphaned SQLite artifacts", files=cleaned_files)
            else:
                logger.debug("No orphaned SQLite artifacts found")

        except Exception as e:
            # No fallar nunca - es limpieza best-effort
            logger.warning("Error during SQLite artifacts cleanup", error=str(e))

    def _get_connection(self) -> sqlite3.Connection:
        """
        Get database connection.

        THREAD SAFETY EXPLAINED:
        ========================
        Why check_same_thread=False is SAFE here:

        1. LOCK SERIALIZATION: execute_async() uses asyncio.Lock() to
           ensure only ONE thread accesses SQLite at a time

        2. SINGLETON PATTERN: Single reused connection, not multiple
           concurrent connections

        3. CONTROLLED THREAD POOL: asyncio.run_in_executor() uses the same
           thread pool, not arbitrary threads

        4. MONO-USER: No real user concurrency

        IMPORTANT: The lock in execute_async() is CRITICAL for this safety.
        Without it, check_same_thread=False would be DANGEROUS.

        ALTERNATIVE CONSIDERED: One connection per thread, but it's overkill
        for a simple mono-user system.
        """
        # Check if database has been closed
        if self._closed:
            raise DatabaseError("Database has been closed")

        if self._connection is None:
            try:
                conn = sqlite3.connect(
                    self.db_path, check_same_thread=False  # Safe due to lock serialization
                )
            except sqlite3.OperationalError as e:
                # Si hay problema de acceso al archivo, intentar limpiar archivos huérfanos
                if "unable to open database file" in str(e).lower():
                    logger.info("Database file access failed, attempting cleanup and retry")
                    self._cleanup_sqlite_artifacts()
                    # Reintentar después de limpieza
                    conn = sqlite3.connect(self.db_path, check_same_thread=False)
                else:
                    raise
            conn.row_factory = sqlite3.Row
            # Enable foreign keys con retry robusto
            retry_sync(
                lambda: conn.execute("PRAGMA foreign_keys = ON"),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
            # CRITICAL: Configure busy_timeout to handle transaction upgrade failures
            # 30 seconds timeout for writes - prevents immediate SQLITE_BUSY errors
            retry_sync(
                lambda: conn.execute("PRAGMA busy_timeout = 30000"),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
            self._connection = conn
        return self._connection

    def close(self):
        """Close database connection to prevent locks and reset singleton.

        SAFETY NOTE: This method should only be called when no async operations
        are in progress. The aggressive closing pattern can cause race conditions
        with concurrent execute_async() operations.
        """
        # Mark as closed FIRST to prevent new operations
        self._closed = True

        # SAFETY: Add a small delay to allow any pending operations to complete
        # This reduces the chance of race conditions with concurrent database operations
        import time

        time.sleep(0.1)  # 100ms delay

        # Close connection (not thread-critical, per-instance operation)
        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                logger.debug("Database connection closed successfully")
            except Exception as e:
                logger.warning("Error closing database connection", error=str(e))

        # CRITICAL: Thread-safe singleton reset
        # This ensures that after closing, get_db_manager() creates a fresh instance
        global _db_manager
        with _db_lock:
            if _db_manager is self:
                _db_manager = None
                logger.debug("Database manager singleton reset")

    def _init_schema(self):
        """
        Inicializa o migra esquema de base de datos.

        Tablas principales:

        1. conversations - Historial de chat
           - Índices en session_id, timestamp
           - task_id para agrupar sesiones

        2. tasks - Agrupación de sesiones
           - Permite recuperar contexto de proyectos
           - Jerarquía Task > Session > Message

        3. task_sessions - Relación many-to-many
           - Conecta tasks con sesiones
           - Permite múltiples sesiones por task

        4. task_summary - Vista agregada
           - Resumen de tasks con conteos
           - Última actividad por task

        5. dream_state - Estado del optimizador
           - Singleton (solo una fila)
           - Métricas de fatiga técnica

        6. dream_insights - Descubrimientos
           - Patrones detectados durante optimización
           - Tipos: PATTERN, CONNECTION, OPTIMIZATION, ARCHITECTURE, BUG_RISK
           - Índice para búsqueda eficiente
        """
        schemas_path = Path(__file__).parent / "database_schemas" / "schemas.sql"
        if not schemas_path.exists():
            logger.error("schemas.sql not found", path=str(schemas_path))
            raise DatabaseError(f"Schema file not found: {schemas_path}")

        with open(schemas_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        conn = self._get_connection()
        assert conn is not None, "Database connection should not be None after _get_connection()"
        try:
            retry_sync(
                lambda: conn.executescript(schema_sql),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
            retry_sync(
                lambda: conn.commit(),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
        except sqlite3.Error as e:
            # Use specific classification for schema errors
            raise _classify_sqlite_error(e)

    @contextmanager
    def transaction(self, isolation_level: str = "IMMEDIATE"):
        """
        Context manager para transacciones seguras.

        CHANGED: Default from DEFERRED to IMMEDIATE to fix race conditions
        ==================================================================

        DEFERRED caused "Node was inserted but could not retrieve ID" errors
        because transactions would upgrade locks mid-transaction, causing
        SQLITE_BUSY errors in concurrent operations.

        IMMEDIATE acquires write locks immediately, preventing race conditions.

        Niveles de aislamiento:
        - IMMEDIATE: Lock al inicio (NEW DEFAULT - prevents race conditions)
        - DEFERRED: Locks al escribir (OLD DEFAULT - caused race conditions)
        - EXCLUSIVE: Lock exclusivo total
        """
        conn = self._get_connection()
        old_isolation = conn.isolation_level

        try:
            conn.isolation_level = isolation_level
            retry_sync(
                lambda: conn.execute("BEGIN"),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
            yield conn
            retry_sync(
                lambda: conn.commit(),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
        except sqlite3.Error as e:
            retry_sync(
                lambda: conn.rollback(),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
            # Use specific classification for transaction errors
            raise _classify_sqlite_error(e)
        except Exception as e:
            retry_sync(
                lambda: conn.rollback(),
                max_attempts=5,
                retry_on=(sqlite3.Error, DatabaseError, Exception),
                logger=logger,
            )
            raise DatabaseError(f"Transaction failed: {e}")
        finally:
            conn.isolation_level = old_isolation

    async def execute_async(
        self, query: str, params: tuple[Any, ...] = (), fetch: Optional[FetchType] = None
    ) -> QueryResult:
        """
        Asynchronous query execution with serialization for thread-safety.

        DESIGN DECISION: MINIMAL validation for local mono-user system
        ================================================================
        We DON'T exhaustively validate parameters because:
        1. Local mono-user system = trust in the developer
        2. SQLite already validates SQL syntax and types
        3. Excessive validation adds unnecessary latency
        4. SQL errors are properly propagated as DatabaseError

        We DO validate:
        - Non-empty query (prevents obvious errors)
        - Reasonable timeout (30s) to prevent hung queries

        Executes SQLite queries in a thread pool to not block the event loop.
        Uses a lock to serialize access and avoid concurrency issues.

        Args:
            query: SQL query to execute
            params: Query parameters
            fetch: Fetch type (ONE, ALL, NONE)

        Returns:
            QueryResult with obtained data

        Raises:
            DatabaseError: If execution fails
        """
        # Ensure lock exists in the correct event loop (lazy creation)
        if self._lock is None:
            self._lock = asyncio.Lock()
        else:
            # Check if lock is bound to current event loop
            try:
                current_loop = asyncio.get_event_loop()
                if hasattr(self._lock, '_loop') and self._lock._loop != current_loop:  # type: ignore
                    # Create new lock for current event loop
                    self._lock = asyncio.Lock()
            except RuntimeError:
                # No event loop running, create new lock
                self._lock = asyncio.Lock()

        # Serialize access with lock to avoid concurrency issues
        async with self._lock:
            loop = asyncio.get_event_loop()

            def _execute():
                """Execute query in separate thread."""
                # Check if database was closed while we were waiting in the executor
                if self._closed:
                    raise DatabaseError("Database was closed during query execution")

                conn = self._get_connection()
                cursor = conn.cursor()

                try:
                    # Double-check if closed after getting connection
                    if self._closed:
                        raise DatabaseError("Database was closed during query execution")

                    # SAFETY: Triple-check before executing the query to prevent access violations
                    # This is the critical point where Windows fatal exceptions occur
                    if self._closed or not self._connection:
                        raise DatabaseError("Database connection was closed during query execution")

                    cursor.execute(query, params)

                    if fetch == FetchType.ONE:
                        data = cursor.fetchone()
                        return QueryResult(
                            data=dict(data) if data else None,
                            rows_affected=cursor.rowcount,
                            last_row_id=cursor.lastrowid,
                        )
                    elif fetch == FetchType.ALL:
                        rows = cursor.fetchall()
                        data = [dict(row) for row in rows]
                        return QueryResult(
                            data=data, rows_affected=cursor.rowcount, last_row_id=None
                        )
                    else:  # FetchType.NONE or None
                        conn.commit()
                        return QueryResult(
                            data=None, rows_affected=cursor.rowcount, last_row_id=cursor.lastrowid
                        )
                except sqlite3.Error as e:
                    conn.rollback()
                    # Use specific SQLite error classification
                    raise _classify_sqlite_error(e)
                finally:
                    cursor.close()

            try:
                # Retry todo el bloque de ejecución en el thread pool
                result = await retry_async(
                    lambda: asyncio.wait_for(
                        loop.run_in_executor(None, _execute), timeout=30.0
                    ),  # Revertido a 30s
                    max_attempts=5,  # Aumentado de 3 a 5 intentos para mejorar success rate
                    initial_delay=1.0,  # Delay original
                    backoff="exponential",  # Backoff exponencial original
                    retry_on=(SQLiteBusyError, DatabaseError, asyncio.TimeoutError),
                    logger=logger,
                )
                return result
            except asyncio.TimeoutError:
                logger.error("Database query timed out after 30 seconds")  # Actualizado mensaje
                raise DatabaseError("Query execution timed out after 30 seconds")
            except Exception as e:
                logger.error("Database query failed", error=str(e))
                raise DatabaseError(f"Failed to execute query: {str(e)}")

    def migrate_schema(self, target_version: int):
        """
        Schema migration system.

        CLARIFICATION: Method intentionally EMPTY
        =========================================
        This is NOT missing functionality, it's an explicit ARCHITECTURAL DECISION.

        WHY WE DON'T IMPLEMENT MIGRATIONS:
        1. ACOLYTE is mono-user = no distributed teams
        2. Schema is stable = infrequent changes
        3. Clean installation = simpler than complex migration
        4. Manual backup = user has full control

        IF IN THE FUTURE we need migrations:
        - Add schema_version table
        - Implement incremental migrations
        - Add automatic rollback

        REFERENCE: Decision #27 in docs/AUDIT_DECISIONS.md
        """
        # Schema is initialized complete in _init_schema()
        # We DON'T need migrations for mono-user system
        pass

    def cleanup_sqlite_artifacts(self) -> None:
        """
        Public method to clean up SQLite artifacts.

        This method provides a safe public interface for cleaning up orphaned
        SQLite WAL and SHM files that may prevent database access.

        Used by maintenance operations and diagnostic tools.
        """
        self._cleanup_sqlite_artifacts()


class InsightStore:
    """
    Specialized store for optimizer insights.

    ⚠️ CORRECT LOCATION - DO NOT MOVE TO SERVICES ⚠️
    =============================================
    InsightStore MUST be in Core because:

    1. IT'S SPECIALIZED INFRASTRUCTURE, not business logic
       - Handles zlib data compression
       - Implements hash-based deduplication
       - Manages inverted indexes

    2. WILL BE USED BY DREAM SERVICE (future)
       - Dream Service is in /dream (when implemented)
       - Dream uses InsightStore as its persistence layer
       - Similar to how all modules use MetricsCollector from Core

    3. FOLLOWS THE ARCHITECTURAL PATTERN
       - Core provides: Infrastructure + Specialized Stores
       - Services provides: Business logic + Orchestration
       - Dream will use: InsightStore from Core to persist

    4. COMPARABLE TO OTHER CORE COMPONENTS
       - MetricsCollector: Used by all modules
       - TokenBudgetManager: Used by several services
       - InsightStore: Used by Dream (specific but infrastructure)

    Features:
    1. Automatic compression (zlib level 9)
    2. Similarity-based deduplication
    3. Inverted index for search
    4. Relevance ranking
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    async def store_insights(
        self, session_id: str, insights: List[Dict[str, Any]], compression_level: int = 9
    ) -> StoreResult:
        """
        Store insights with deduplication.

        Process:
        1. Calculate content hash
        2. Search for duplicates (similarity > 0.85)
        3. Compress unique data
        4. Update inverted index
        5. Calculate statistics
        """
        logger.debug("Storing insights", session_id=session_id, count=len(insights))
        stored_count = 0
        duplicate_count = 0

        for insight in insights:
            # Generate unique ID
            insight_id = generate_id()

            # DECISION #32: Accept duplicates for MVP
            # Dream can generate similar insights in different cycles
            # It's normal and expected to have some duplicates
            # FUTURE: If annoying, implement content hashing

            # Compress entities and code_references
            entities_json = json.dumps(insight.get("entities", []))
            code_refs_json = json.dumps(insight.get("code_references", []))

            entities_compressed = zlib.compress(entities_json.encode(), level=compression_level)
            code_refs_compressed = zlib.compress(code_refs_json.encode(), level=compression_level)

            query = """
                INSERT INTO dream_insights (
                    id, session_id, insight_type, title, description,
                    entities_involved, code_references, confidence, impact
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            params = (
                insight_id,
                session_id,
                insight["type"].upper(),  # Enum in UPPERCASE
                insight["title"],
                insight["description"],
                entities_compressed,
                code_refs_compressed,
                insight.get("confidence", 0.5),
                insight.get("impact", "MEDIUM").upper(),
            )

            await self.db.execute_async(query, params)
            stored_count += 1

        result = StoreResult(
            success=True,
            id=session_id,
            message=f"Stored {stored_count} insights, {duplicate_count} duplicates skipped",
            stats={"stored": stored_count, "duplicates": duplicate_count, "total": len(insights)},
        )

        logger.info("Insights stored successfully", session_id=session_id, stored=stored_count)
        return result


# Global singleton for the entire application
_db_manager = None
# Thread lock for safe singleton management
_db_lock = threading.Lock()


def get_db_manager() -> DatabaseManager:
    """Get the singleton DatabaseManager instance with thread safety.

    SAFETY NOTE: This function ensures that only one DatabaseManager instance
    exists at a time, preventing conflicts with concurrent database operations.
    """
    global _db_manager
    # Thread-safe singleton creation
    with _db_lock:
        if _db_manager is None:
            _db_manager = DatabaseManager()
        # SAFETY: Return a reference to the existing manager if it's not closed
        # This prevents issues if close() was called from another thread
        elif getattr(_db_manager, '_closed', False):
            # If the manager was closed, create a new one
            _db_manager = DatabaseManager()
        return _db_manager
