"""
Persistent cache for embeddings with deferred write.

Extends ContextAwareCache with disk persistence every 5 minutes,
keeping all operations 100% in memory during normal use.
"""

import threading
import time
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Union, Any
import json

from acolyte.core.logging import logger
from acolyte.embeddings.cache import ContextAwareCache, CacheEntry
from acolyte.embeddings.types import EmbeddingVector
from acolyte.embeddings.context import RichCodeContext
from acolyte.models.chunk import Chunk


class SmartPersistentCache(ContextAwareCache):
    """LRU cache with deferred disk persistence.

    Keeps all operations in memory for maximum performance,
    saving to disk periodically (every 5 minutes) or on close.

    The persistence format uses numpy compressed (.npz) for efficiency.
    """

    # Cache format version (increment if changed)
    CACHE_VERSION = 1

    def __init__(
        self,
        max_size: int = 10000,
        ttl_seconds: int = 3600,
        save_interval: int = 300,
        cache_dir: Optional[Path] = None,
    ):
        """Initializes cache with persistence.

        Args:
            max_size: Maximum number of entries
            ttl_seconds: TTL in seconds
            save_interval: Save interval in seconds (default: 5 min)
            cache_dir: Directory for cache (default: project-aware location)
        """
        super().__init__(max_size, ttl_seconds)

        self._save_interval = save_interval
        self._dirty = False
        self._last_save = time.time()
        self._save_lock = threading.Lock()

        # Configure cache directory
        if cache_dir is None:
            self._cache_dir = self._get_cache_path()
        else:
            self._cache_dir = cache_dir
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_file = self._cache_dir / "embeddings.npz"
        self._meta_file = self._cache_dir / "embeddings.meta"

        # Load previous state if exists
        self._load_from_disk()

        # Start periodic save thread
        self._start_periodic_save()

        logger.info(
            "SmartPersistentCache initialized",
            max_size=max_size,
            ttl_seconds=ttl_seconds,
            save_interval=save_interval,
            cache_file=str(self._cache_file),
        )

    def _get_cache_path(self) -> Path:
        """Get the correct path for embeddings cache.

        CLEAN PROJECT ARCHITECTURE:
        - If .acolyte.project exists: use ~/.acolyte/projects/{id}/data/embeddings_cache/
        - Otherwise (during development): use ./data/embeddings_cache/
        """
        # Check if we're in a configured project
        project_file = Path.cwd() / ".acolyte.project"

        if project_file.exists():
            try:
                import yaml

                with open(project_file) as f:
                    project_data = yaml.safe_load(f)
                    project_id = project_data.get("project_id")

                if project_id:
                    # Use global project directory
                    global_cache_dir = (
                        Path.home()
                        / ".acolyte"
                        / "projects"
                        / project_id
                        / "data"
                        / "embeddings_cache"
                    )
                    return global_cache_dir
            except Exception as e:
                logger.warning("Failed to read project file, using local data", error=str(e))

        # Fallback for development
        return Path("data") / "embeddings_cache"

    def _start_periodic_save(self):
        """Starts periodic background saving."""
        # Flag to signal thread shutdown
        self._shutdown_flag = threading.Event()

        def save_loop():
            while not self._shutdown_flag.is_set():
                # Use shutdown_flag.wait() instead of time.sleep() for immediate response
                if self._shutdown_flag.wait(timeout=self._save_interval):
                    # Shutdown was signaled
                    break

                # Only save if still running and dirty
                if not self._shutdown_flag.is_set() and self._dirty:
                    try:
                        self.save_to_disk()
                    except Exception as e:
                        # Don't crash thread on save errors during shutdown
                        if not self._shutdown_flag.is_set():
                            logger.error("Error in save_loop", error=str(e))

        self._save_thread = threading.Thread(target=save_loop, daemon=True)
        self._save_thread.start()

    def _load_from_disk(self):
        """Loads the cache from disk if it exists and is valid."""
        if not self._cache_file.exists() or not self._meta_file.exists():
            logger.debug("No previous cache found")
            return

        try:
            # Check metadata first
            with open(self._meta_file, 'r') as f:
                metadata = json.load(f)

            if metadata.get('version') != self.CACHE_VERSION:
                logger.warning(
                    "Incompatible cache version",
                    cache_version=metadata.get('version'),
                    expected=self.CACHE_VERSION,
                )
                return

            # Load cache data
            data = np.load(self._cache_file, allow_pickle=True)

            # Rebuild cache
            keys = data['keys']
            embeddings = data['embeddings']
            created_ats = data['created_ats']

            current_time = time.time()
            loaded_count = 0
            expired_count = 0

            for i, key in enumerate(keys):
                # Check TTL on load
                if current_time - created_ats[i] > self.ttl_seconds:
                    expired_count += 1
                    continue

                # Rebuild EmbeddingVector
                embedding = EmbeddingVector(embeddings[i])
                entry = CacheEntry(embedding=embedding, created_at=created_ats[i])

                # Add directly to the internal OrderedDict
                self._cache[key] = entry  # type: ignore[attr-defined]
                loaded_count += 1

            logger.info(
                "Cache loaded from disk",
                loaded=loaded_count,
                expired=expired_count,
                total=len(keys),
            )

        except Exception as e:
            logger.error(
                "Error loading cache from disk", error=str(e), cache_file=str(self._cache_file)
            )
            # On error, start with empty cache
            self._cache.clear()  # type: ignore[attr-defined]

    def save_to_disk(self):
        """Saves the cache to disk if there are changes."""
        if not self._dirty:
            return

        with self._save_lock:
            try:
                if not self._cache:  # type: ignore[attr-defined]
                    logger.debug("Empty cache, nothing to save")
                    return

                # Extract data from cache
                keys = []
                embeddings = []
                created_ats = []

                for key, entry in self._cache.items():  # type: ignore[attr-defined]
                    keys.append(key)
                    embeddings.append(entry.embedding.numpy)
                    created_ats.append(entry.created_at)

                # Save with numpy compressed
                np.savez_compressed(
                    self._cache_file,
                    keys=np.array(keys),
                    embeddings=np.array(embeddings),
                    created_ats=np.array(created_ats),
                )

                # Save metadata
                metadata = {
                    'version': self.CACHE_VERSION,
                    'saved_at': time.time(),
                    'entries': len(keys),
                    'max_size': self.max_size,
                    'ttl_seconds': self.ttl_seconds,
                }

                with open(self._meta_file, 'w') as f:
                    json.dump(metadata, f, indent=2)

                self._dirty = False
                self._last_save = time.time()

                # Calculate file size
                file_size_mb = self._cache_file.stat().st_size / (1024 * 1024)

                logger.info(
                    "Cache saved to disk", entries=len(keys), file_size_mb=f"{file_size_mb:.2f}"
                )

            except Exception as e:
                logger.error(
                    "Error saving cache to disk", error=str(e), cache_file=str(self._cache_file)
                )

    def set(
        self,
        text: Union[str, Chunk],
        context: Optional[RichCodeContext],
        embedding: EmbeddingVector,
    ):
        """Saves embedding in cache marking it as dirty."""
        super().set(text, context, embedding)
        self._dirty = True

        # Auto-save if too much time has passed
        if time.time() - self._last_save > self._save_interval:
            self.save_to_disk()

    def clear(self):
        """Clears the cache and marks it as dirty."""
        super().clear()
        self._dirty = True

    def cleanup_expired(self) -> int:
        """Cleans up expired entries and marks as dirty if there were changes."""
        removed = super().cleanup_expired()
        if removed > 0:
            self._dirty = True
        return removed

    def close(self):
        """Closes the cache saving pending changes.

        Explicit method to call when finishing cache usage.
        Avoids issues with __del__ during shutdown.
        """
        try:
            # Signal shutdown to background thread FIRST
            if hasattr(self, '_shutdown_flag'):
                self._shutdown_flag.set()

            # Wait for thread to finish gracefully (with timeout)
            if hasattr(self, '_save_thread') and self._save_thread.is_alive():
                self._save_thread.join(timeout=2.0)  # Wait max 2 seconds
                if self._save_thread.is_alive():
                    logger.warning("Save thread did not stop gracefully within timeout")

            # Save if there are pending changes (after thread stops)
            if hasattr(self, '_dirty') and self._dirty:
                logger.debug("Saving cache before closing")
                self.save_to_disk()

        except Exception as e:
            logger.error("Error in cache cleanup", error=str(e))

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures saving."""
        self.close()
        return False  # Do not suppress exceptions

    def __del__(self):
        """Destructor as fallback - tries to save but does not guarantee."""
        # Keep a minimal __del__ as a last resort
        # but recommended usage is with context manager or close()
        try:
            # Signal shutdown first
            if hasattr(self, '_shutdown_flag'):
                self._shutdown_flag.set()

            # Try to save if dirty
            if hasattr(self, '_dirty') and self._dirty:
                self.save_to_disk()
        except Exception:
            # Silence all errors during destruction
            pass

    def get_persistent_stats(self) -> Dict[str, Any]:
        """Returns statistics including persistence info."""
        stats = self.get_stats()

        # Add persistence info
        if self._cache_file.exists():
            file_size = self._cache_file.stat().st_size / (1024 * 1024)
            stats['persistent'] = {  # type: ignore[index]
                'file_size_mb': f"{file_size:.2f}",
                'last_save': self._last_save,
                'time_since_save': time.time() - self._last_save,
                'dirty': self._dirty,
                'save_interval': self._save_interval,
            }
        else:
            stats['persistent'] = {'file_exists': False, 'dirty': self._dirty}  # type: ignore[index]

        return stats  # type: ignore[return-value]
