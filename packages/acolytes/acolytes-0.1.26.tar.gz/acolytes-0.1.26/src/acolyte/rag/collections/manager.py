# 🔧 Collection Manager - Simple Weaviate Collections Management

"""
Minimalist manager to create and manage ACOLYTE's 5 collections in Weaviate.
We DON'T need complex abstractions - Weaviate already has everything we need.

Important changes:
- Uses CollectionName enum instead of hardcoded strings
- Removed unused methods (delete_collection, validate_chunk_for_collection)
- Captures specific Weaviate exceptions
- Removed CLI (not used)
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import weaviate  # type: ignore
from acolyte.core.logging import logger
from acolyte.core.exceptions import DatabaseError
from acolyte.core.secure_config import Settings
from acolyte.rag.collections.collection_names import CollectionName
import os

# Import only valid exceptions from weaviate.exceptions
from weaviate.exceptions import (  # type: ignore
    WeaviateBaseError as WeaviateException,
    UnexpectedStatusCodeException,
    ObjectAlreadyExistsException,
)


class CollectionManager:
    """
    Simple Weaviate collections manager.

    Only does what's necessary:
    - Create collections from schemas.json
    - Validate they exist
    - Basic management operations
    """

    def __init__(self, weaviate_url: Optional[str] = None):
        """
        Initialize the manager.

        Args:
            weaviate_url: Weaviate URL (default: reads from .acolyte)
        """
        self.config = Settings()

        # Weaviate URL from config or parameter
        if not weaviate_url:
            weaviate_port = self.config.get("ports.weaviate", 8080)
            weaviate_url = os.getenv("WEAVIATE_URL", f"http://localhost:{weaviate_port}")
        self.weaviate_url = weaviate_url
        self.client = None
        self._schemas = None

    def connect(self):
        """Connect to Weaviate."""
        try:
            self.client = weaviate.Client(self.weaviate_url)
            if not self.client.is_ready():
                raise DatabaseError("Weaviate is not ready")
            logger.info("Connected to Weaviate", weaviate_url=self.weaviate_url)
        except WeaviateException as e:
            logger.error("Weaviate error", error=str(e))
            raise DatabaseError("Error connecting to Weaviate: " + str(e))
        except Exception as e:
            logger.error("Unexpected error connecting to Weaviate", error=str(e))
            raise DatabaseError("Unexpected error: " + str(e))

    def disconnect(self):
        """Disconnect from Weaviate."""
        if self.client:
            # Weaviate client doesn't have explicit close method
            self.client = None
            logger.info("Disconnected from Weaviate")

    @property
    def schemas(self) -> Dict[str, Any]:
        """Load schemas from schemas.json (lazy loading)."""
        if self._schemas is None:
            schema_path = Path(__file__).parent / "schemas.json"

            # Validate file exists
            if not schema_path.exists():
                logger.error("schemas.json file not found", path=str(schema_path))
                raise DatabaseError("schemas.json file not found")

            try:
                with open(schema_path, "r") as f:
                    self._schemas = json.load(f)
                logger.info("Schemas loaded from schemas.json")
            except json.JSONDecodeError as e:
                logger.error("Error parsing schemas.json", error=str(e))
                raise DatabaseError("schemas.json is not valid JSON: " + str(e))
            except Exception as e:
                logger.error("Error loading schemas", error=str(e))
                raise DatabaseError("Cannot load schemas: " + str(e))
        return self._schemas

    def create_all_collections(self):
        """
        Create all collections defined in schemas.json.

        The 5 mandatory collections defined in CollectionName enum:
        - Conversation
        - CodeChunk
        - Document
        - Task
        - DreamInsight
        """
        if not self.client:
            self.connect()

        created = 0
        expected_collections = CollectionName.list_all()

        for collection_def in self.schemas.get("collections", []):
            collection_name = collection_def["class"]

            # Validate it's an expected collection
            if collection_name not in expected_collections:
                logger.warning(
                    "Collection not in CollectionName enum", collection_name=collection_name
                )

            if self.collection_exists(collection_name):
                logger.info("Collection already exists", collection_name=collection_name)
                continue

            try:
                self._create_collection(collection_def)
                created += 1
                logger.info("Collection created", collection_name=collection_name)
            except ObjectAlreadyExistsException:
                logger.info(
                    "Collection already exists (race condition)", collection_name=collection_name
                )
            except UnexpectedStatusCodeException as e:
                logger.error(
                    "HTTP error creating collection", collection_name=collection_name, error=str(e)
                )
                raise DatabaseError("Weaviate HTTP error: " + str(e))
            except WeaviateException as e:
                logger.error(
                    "Weaviate error creating collection",
                    collection_name=collection_name,
                    error=str(e),
                )
                raise DatabaseError("Weaviate error: " + str(e))
            except Exception as e:
                logger.error(
                    "Unexpected error creating collection",
                    collection_name=collection_name,
                    error=str(e),
                )
                raise

        logger.info("Created new collections", count=created)
        return created

    def collection_exists(self, name: str) -> bool:
        """Check if a collection exists."""
        if not self.client:
            self.connect()
        if not self.client:
            logger.error("Could not initialize Weaviate client")
            logger.info("[TRACE] Weaviate client initialization failed")
            return False
        try:
            schema = self.client.schema.get()
            return any(c["class"] == name for c in schema.get("classes", []))
        except WeaviateException as e:
            logger.error("Weaviate error checking collection", name=name, error=str(e))
            return False
        except Exception as e:
            logger.error("Error checking collection", name=name, error=str(e))
            return False

    def _create_collection(self, collection_def: Dict[str, Any]):
        """
        Create an individual collection.

        Args:
            collection_def: Collection definition from schemas.json
        """
        # Base configuration
        class_obj = {
            "class": collection_def["class"],
            "description": collection_def.get("description", ""),
            "vectorizer": collection_def.get("vectorizer", "none"),  # none = external embeddings
            "properties": collection_def.get("properties", []),
        }

        # Vector index configuration (HNSW)
        if "indexing_config" in self.schemas:
            vector_config = self.schemas["indexing_config"].get("vectorIndexConfig", {})
            class_obj["vectorIndexConfig"] = vector_config

        if not self.client:
            logger.info("[TRACE] Weaviate client not initialized in _create_collection")
            raise DatabaseError("Weaviate client not initialized")
        # Create the collection
        self.client.schema.create_class(class_obj)

    def get_collection_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get collection information.

        Args:
            name: Collection name (use CollectionName enum)

        Returns:
            Collection info or None if doesn't exist
        """
        if not self.client:
            self.connect()
        if not self.client:
            logger.error("Could not initialize Weaviate client")
            logger.info("[TRACE] Weaviate client initialization failed in get_collection_info")
            return None
        try:
            schema = self.client.schema.get()
            for class_def in schema.get("classes", []):
                if class_def["class"] == name:
                    # Add object count
                    count = self._get_object_count(name)
                    class_def["object_count"] = count
                    return class_def
            return None
        except WeaviateException as e:
            logger.error("Weaviate error getting info", name=name, error=str(e))
            return None
        except Exception as e:
            logger.error("Error getting info", name=name, error=str(e))
            logger.info("[TRACE] General exception getting collection info")
            return None

    def _get_object_count(self, collection_name: str) -> int:
        """Get the number of objects in a collection."""
        if not self.client:
            logger.error("Could not initialize Weaviate client")
            logger.info("[TRACE] Weaviate client initialization failed in _get_object_count")
            return 0
        try:
            result = self.client.query.aggregate(collection_name).with_meta_count().do()
            return result["data"]["Aggregate"][collection_name][0]["meta"]["count"]
        except WeaviateException as e:
            logger.error(
                "Weaviate error getting count", collection_name=collection_name, error=str(e)
            )
            logger.info("[TRACE] Weaviate exception in aggregate query")
            return 0
        except Exception as e:
            logger.error(
                "Error getting object count", collection_name=collection_name, error=str(e)
            )
            logger.info("[TRACE] General exception getting object count")
            return 0

    def get_all_collections(self) -> List[str]:
        """
        List all existing collections.

        Returns:
            List of collection names
        """
        if not self.client:
            self.connect()
        if not self.client:
            logger.error("Could not initialize Weaviate client")
            logger.info("[TRACE] Weaviate client initialization failed in get_all_collections")
            return []
        try:
            schema = self.client.schema.get()
            return [c["class"] for c in schema.get("classes", [])]
        except WeaviateException as e:
            logger.error("Weaviate error listing collections", error=str(e))
            logger.info("[TRACE] Weaviate exception listing collections")
            return []
        except Exception as e:
            logger.error("Error listing collections", error=str(e))
            logger.info("[TRACE] General exception listing collections")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics for all collections.

        Returns:
            Dict with statistics per collection
        """
        if not self.client:
            self.connect()
        if not self.client:
            logger.error("Could not initialize Weaviate client")
            logger.info("[TRACE] Weaviate client initialization failed in get_statistics")
            return {"total_objects": 0, "collections": {}}
        stats = {"total_objects": 0, "collections": {}}
        for collection in self.get_all_collections():
            info = self.get_collection_info(collection)
            if info:
                count = info.get("object_count", 0)
                stats["collections"][collection] = {
                    "object_count": count,
                    "properties": len(info.get("properties", [])),
                    "vectorizer": info.get("vectorizer", "none"),
                }
                stats["total_objects"] += count
        return stats

    def health_check(self) -> Dict[str, Any]:
        """
        Check collection system health.

        Returns:
            Health status with details
        """
        health = {"healthy": False, "weaviate_ready": False, "collections_ok": False, "details": {}}
        try:
            # Check connection
            if not self.client:
                self.connect()
            if not self.client:
                health["details"]["error"] = "Could not initialize Weaviate client"
                logger.info("[TRACE] Weaviate client initialization failed in health_check")
                return health
            health["weaviate_ready"] = self.client.is_ready()
            # Check mandatory collections using enum
            required = CollectionName.list_all()
            existing = self.get_all_collections()
            missing = [c for c in required if c not in existing]
            health["details"]["missing_collections"] = missing
            health["collections_ok"] = len(missing) == 0
            # General status
            health["healthy"] = health["weaviate_ready"] and health["collections_ok"]
        except WeaviateException as e:
            health["details"]["error"] = "Weaviate error: " + str(e)
        except Exception as e:
            health["details"]["error"] = str(e)
        return health


# Helper function for quick use
def get_collection_manager(weaviate_url: Optional[str] = None) -> CollectionManager:
    """
    Factory helper to get a configured manager.

    Args:
        weaviate_url: Optional Weaviate URL

    Returns:
        CollectionManager ready to use
    """
    manager = CollectionManager(weaviate_url)
    manager.connect()
    return manager
