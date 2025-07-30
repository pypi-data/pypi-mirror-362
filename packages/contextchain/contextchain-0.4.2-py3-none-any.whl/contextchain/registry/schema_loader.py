import os
from typing import Dict, Any, List
import logging
from contextchain.engine.validator import validate_schema
from contextchain.db.mongo_client import get_mongo_client
import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VersionManager:
    _instance = None
    supported_versions = set()  # Dynamic set of supported versions

    def __new__(cls, client=None, db_name="contextchain_db"):
        if cls._instance is None:
            cls._instance = super(VersionManager, cls).__new__(cls)
            try:
                cls._instance.client = client or get_mongo_client()
                cls._instance.db = cls._instance.client[db_name]
                cls._instance.collection = cls._instance.db["schema_registry"]
                cls._instance.supported_versions.add("0.1.0")  # Initial supported version
            except Exception as e:
                logger.error(f"Failed to initialize MongoClient: {str(e)}")
                cls._instance.client = None
        return cls._instance

    def get_version(self, schema: Dict[str, Any]) -> str:
        """Extract or generate the version with fallback."""
        raw_version = schema.get("schema_version", "0.1.0")
        if not raw_version.startswith("v"):
            raw_version = f"v{raw_version}"
        parts = [int(p) for p in raw_version.replace("v", "").split(".")]
        if len(parts) != 3:
            logger.warning(f"Invalid version format {raw_version}. Using 0.1.0")
            return "v0.1.0"
        return raw_version

    def increment_version(self, pipeline_id: str, increment_type: str = "patch") -> str:
        """Increment the version based on the latest version (manual control disabled)."""
        versions = self.list_versions(pipeline_id)
        if not versions:
            return "v0.1.0"  # Initial version for new pipeline
        latest = max(versions, key=lambda x: [int(p) for p in x["schema_version"].replace("v", "").split(".")])
        major, minor, patch = [int(p) for p in latest["schema_version"].replace("v", "").split(".")]
        if increment_type == "major":
            major += 1; minor = 0; patch = 0
        elif increment_type == "minor":
            minor += 1; patch = 0
        else:  # patch
            patch += 1
        new_version = f"v{major}.{minor}.{patch}"
        self.supported_versions.add(new_version)
        return new_version

    def push_schema(self, pipeline_id: str, schema: Dict[str, Any], increment: bool = False) -> str:
        """Save a schema version to MongoDB with manual version control."""
        try:
            validate_schema(schema)
        except ValueError as e:
            logger.error(f"Schema validation failed for {pipeline_id}: {str(e)}")
            raise

        version = self.get_version(schema)
        if increment:
            logger.warning("Automatic version incrementation is disabled. Use schema_version field manually.")
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        existing_version = self.collection.find_one({"pipeline_id": pipeline_id, "schema_version": version})
        if existing_version and existing_version["schema_version"] == version:
            logger.error(f"Version {version} already exists for pipeline {pipeline_id}")
            raise ValueError(f"Duplicate version {version} detected for pipeline {pipeline_id}. Please use a unique version number.")

        self.collection.update_many({"pipeline_id": pipeline_id}, {"$set": {"is_latest": False}})
        schema_doc = {
            "pipeline_id": pipeline_id,
            "schema": schema,
            "schema_version": version,
            "created_at": timestamp,
            "is_latest": True
        }
        result = self.collection.insert_one(schema_doc)
        logger.info(f"Pushed schema for {pipeline_id} with version {version} at {timestamp} (schema: {json.dumps(schema)})")
        return version

    def list_versions(self, pipeline_id: str) -> List[Dict[str, Any]]:
        """Retrieve all versions for a pipeline."""
        versions = list(self.collection.find({"pipeline_id": pipeline_id}).sort("created_at", -1))
        if not versions:
            logger.warning(f"No versions found for pipeline {pipeline_id}")
        else:
            logger.debug(f"Found versions for {pipeline_id}: {[v['schema_version'] for v in versions]}")
        return versions

    def rollback_version(self, pipeline_id: str, version: str) -> Dict[str, Any]:
        """Rollback to a specific version."""
        version_doc = self.collection.find_one({"pipeline_id": pipeline_id, "schema_version": version})
        if not version_doc:
            logger.error(f"No version {version} found for {pipeline_id}")
            raise KeyError(f"Version {version} not found for {pipeline_id}")
        self.collection.update_many({"pipeline_id": pipeline_id}, {"$set": {"is_latest": False}})
        self.collection.update_one({"_id": version_doc["_id"]}, {"$set": {"is_latest": True}})
        logger.info(f"Rolled back {pipeline_id} to version {version}")
        return version_doc["schema"]

    def get_latest_schema(self, pipeline_id: str) -> Dict[str, Any]:
        """Retrieve the latest schema version for a pipeline based on semantic versioning."""
        versions = self.list_versions(pipeline_id)
        if not versions:
            logger.error(f"No versions found for pipeline {pipeline_id}")
            return None
        latest = max(versions, key=lambda x: [int(p) for p in x["schema_version"].replace("v", "").split(".")])
        logger.info(f"Retrieved latest schema version {latest['schema_version']} for pipeline {pipeline_id}")
        return latest["schema"]

    def close(self):
        """Close the MongoDB client."""
        if hasattr(self._instance, 'client') and self._instance.client:
            self._instance.client.close()
            logger.info("MongoDB client closed")
            self._instance.client = None

# Module-level functions for CLI compatibility
def push_schema(client, db_name: str, schema: Dict[str, Any], increment: bool = False) -> str:
    vm = VersionManager(client, db_name)
    return vm.push_schema(schema["pipeline_id"], schema, increment)

def list_versions(client, db_name: str, pipeline_id: str) -> List[Dict[str, Any]]:
    vm = VersionManager(client, db_name)
    return vm.list_versions(pipeline_id)

def rollback_version(client, db_name: str, pipeline_id: str, version: str) -> Dict[str, Any]:
    vm = VersionManager(client, db_name)
    return vm.rollback_version(pipeline_id, version)

class SchemaLoader:
    def __init__(self, schema_dir: str = "schemas"):
        self.schema_dir = schema_dir
        self.version_manager = VersionManager()

    def load_from_file(self, filename: str) -> bool:
        """Load a schema from a JSON file and register it without automatic increment."""
        file_path = os.path.join(self.schema_dir, filename)
        if not os.path.exists(file_path):
            logger.error(f"Schema file {file_path} not found")
            return False

        try:
            with open(file_path, 'r') as f:
                schema = json.load(f)
            validate_schema(schema)
            self.version_manager.push_schema(schema["pipeline_id"], schema, increment=False)
            logger.info(f"Loaded and registered schema from {file_path} with version {schema['schema_version']}")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error loading schema from {file_path}: {str(e)}")
            return False

    def load_all(self) -> int:
        """Load all schemas from the schema directory."""
        if not os.path.exists(self.schema_dir):
            logger.error(f"Schema directory {self.schema_dir} does not exist")
            return 0
        loaded_count = 0
        for filename in os.listdir(self.schema_dir):
            if filename.endswith('.json'):
                if self.load_from_file(filename):
                    loaded_count += 1
        return loaded_count

def load_schema(client, db_name: str, pipeline_id: str, version: str = None) -> Dict[str, Any]:
    """Load a schema from MongoDB based on pipeline ID and optional version."""
    vm = VersionManager(client, db_name)
    versions = vm.list_versions(pipeline_id)
    logger.debug(f"Versions retrieved for {pipeline_id}: {versions}")  # Add debug logging
    if not versions:
        logger.error(f"No versions found for pipeline {pipeline_id} in MongoDB")
        return None
    if version:
        target_version = next((v for v in versions if v["schema_version"] == version), None)
        if not target_version:
            logger.error(f"Version {version} not found for pipeline {pipeline_id}")
            return None
        logger.info(f"Loaded schema version {version} for pipeline {pipeline_id}")
        return target_version["schema"]
    latest_schema = vm.get_latest_schema(pipeline_id)
    if latest_schema:
        logger.info(f"Loaded latest schema version for pipeline {pipeline_id}")
        return latest_schema
    logger.warning(f"No latest schema found, falling back to first version for pipeline {pipeline_id}")
    return versions[0]["schema"]  # Fallback to first version if no latest