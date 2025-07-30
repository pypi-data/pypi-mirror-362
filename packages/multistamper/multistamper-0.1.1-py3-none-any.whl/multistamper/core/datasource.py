"""Data source interface and implementation for local file system data storage."""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Dict, List, Optional

from dotenv import dotenv_values
from vbase import VBaseStringObject

NOT_IN_COLLECTION = "not_in_collection"

COLLECTION_CONFIG_JSON = "collection_config.json"
COLLECTION_CONFIG_DOTENV = ".env.collection_config"

USER_CONFIG_JSON = "env.json"
USER_CONFIG_DOTENV = ".env"


@dataclass
class FileWithCID:
    """Data structure for a file with its CID."""

    file_path: Path
    object_cid: str


class AbstractDataSource(ABC):
    """Abstract base class for data sources."""

    @abstractmethod
    def load_users(self) -> Dict:
        """Load user configurations from the data source."""

    @abstractmethod
    def load_collections(self, user_dir: str) -> List[Dict]:
        """Load collections for a specific user directory from the data source."""

    @abstractmethod
    def get_files_for_collection(self, collection_path: Path) -> List[FileWithCID]:
        """Get list of FileWithCID objects for each file in the collection,"""


class LocalDataSource(AbstractDataSource):
    """Local file system data source implementation."""

    def __init__(self, users_root: Path):
        self.users_root = users_root
        self.user_configs = {}

    def load_user_config(self, user_dir) -> Dict[str, str]:
        """Load user configuration from the local file system."""
        if user_dir.is_dir():
            user_config_path = user_dir / USER_CONFIG_JSON
            if user_config_path.exists():
                with open(user_config_path, encoding="utf-8") as f:
                    meta = json.load(f)
                    data = {k.lower(): v for k, v in meta.items()}
                    return data

            env_path = user_dir / USER_CONFIG_DOTENV
            if env_path.exists():
                meta = dotenv_values(env_path)
                data = {k.lower(): v for k, v in meta.items()}
                return data
        return {}

    def load_user_collection_config(self, user_dir: Path) -> Dict:
        """Load user collection configuration from the local file system."""
        if user_dir and user_dir.name == NOT_IN_COLLECTION:
            return {
                "folder_name": NOT_IN_COLLECTION,
                "collection_path": user_dir,
                "collection_name": NOT_IN_COLLECTION,
                "collection_cid": None,
            }

        collection_config_path = user_dir / COLLECTION_CONFIG_JSON
        if collection_config_path.exists():
            with open(collection_config_path, encoding="utf-8") as f:
                config = json.load(f)
                collection_cid = config.get("collection_cid")
                collection_name = config.get("collection_name")
                folder_name = config.get("folder_name")
                return {
                    "folder_name": folder_name,
                    "collection_path": user_dir,
                    "collection_name": collection_name,
                    "collection_cid": collection_cid,
                }

        env_path = user_dir / COLLECTION_CONFIG_DOTENV
        if env_path.exists():
            env_vars = dotenv_values(env_path)
            return {
                "folder_name": user_dir,
                "collection_path": user_dir,
                "collection_name": user_dir.name,
                "collection_cid": env_vars.get("COLLECTION_CID"),
            }

        return {}

    def load_users(self) -> Dict[str, Dict[str, List[Dict]]]:
        """Load user configurations from the local file system."""
        users_config = {"users": {}}
        for user_dir in self.users_root.iterdir():
            # load user configuration
            user_config = self.load_user_config(user_dir)
            # load collections for the user
            collections = (
                self.load_collections(user_dir.name) if user_dir.is_dir() else []
            )
            # add user collections to user config
            user_config["collections"] = collections
            # add user config to users_config, by user directory name
            users_config["users"][user_dir.name] = user_config

        return users_config

    def load_collections(self, user_dir: str) -> List[Dict]:
        """Load collections for a specific user."""
        collections = []
        user_path = self.users_root / user_dir
        collections_path = user_path / "collections"
        if collections_path.exists():
            for item in collections_path.iterdir():
                if item.is_dir():
                    loaded_collection = self.load_user_collection_config(item)
                    collections.append(loaded_collection)

        uncategorized_path = user_path / NOT_IN_COLLECTION
        if uncategorized_path.exists():
            loaded_collection = self.load_user_collection_config(uncategorized_path)
            collections.append(loaded_collection)
        return collections

    def get_files_for_collection(self, collection_path: Path) -> List[FileWithCID]:
        """
        Get list of FileWithCID objects for each file
        in the collection, excluding known config files.

        Returns:
            List[FileWithCID]: List of FileWithCID(file_path, object_cid)
        """
        ignore_files = {COLLECTION_CONFIG_JSON, COLLECTION_CONFIG_DOTENV}
        ignore_folders = "archive"
        result: List[FileWithCID] = []

        for file_path in collection_path.iterdir():
            if file_path.is_dir() and file_path.name in ignore_folders:
                continue

            if file_path.is_file() and file_path.name not in ignore_files:
                try:
                    with file_path.open("rb") as f:
                        object_cid = self.get_object_cid_for_file(f)
                    result.append(
                        FileWithCID(file_path=file_path, object_cid=object_cid)
                    )
                # pylint: disable=broad-exception-caught
                except Exception as e:
                    print(f"Failed to process {file_path}: {e}")
                    raise RuntimeError(f"Failed to process {file_path}: {e}") from e

        return result

    def get_object_cid_for_file(self, file: IO[bytes]) -> Optional[str]:
        """
        Get the object CID for a given UTF-8-encoded file.
        """
        if not file:
            return None

        # Read and decode the file
        file_bytes = file.read()
        try:
            file_str = file_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError("Invalid UTF-8 encoding in file.") from e
        finally:
            file.seek(0)
        return VBaseStringObject(init_data=file_str).get_cid()
