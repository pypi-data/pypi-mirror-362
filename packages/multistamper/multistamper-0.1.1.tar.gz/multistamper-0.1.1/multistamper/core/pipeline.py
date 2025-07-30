"""VBase Processing Pipeline for Stamping Files"""

import datetime
import json
import logging
import os
import shutil
from pathlib import Path
from typing import Dict, List

from .apiclient import ApiClient
from .datasource import AbstractDataSource, FileWithCID

logger = logging.getLogger(__name__)


class Pipeline:
    """Pipeline for processing and stamping files in vBase collections."""

    def __init__(self, data_source: AbstractDataSource, stamping_client: ApiClient):
        """Initialize the processing pipeline with a data source and a stamping client."""
        self.data_source = data_source
        self.stamping_client = stamping_client
        self.stamped_files = []

    def preview(self, current_user: str) -> List[Dict]:
        """Preview the files that will be processed for the current user."""
        collections = self.data_source.load_collections(current_user)
        preview_list = []
        for collection in collections:
            collection_path = collection.get("collection_path")
            collection_name = collection.get("collection_name")
            collection_cid = collection.get("collection_cid")
            objects = self.data_source.get_files_for_collection(collection_path)
            objects, _ = self.get_filtered_files(objects, collection_cid=collection_cid)
            print(f"Previewing collection: {collection_name} (CID: {collection_cid})")
            for file_object in objects:
                file_path = file_object.file_path
                preview_list.append(
                    {
                        "file": file_path.name,
                        "object_cid": file_object.object_cid,
                        "collection": collection_name,
                        "collection_cid": collection_cid,
                        "path": str(file_path),
                        "user": current_user,
                    }
                )
        return preview_list

    def log_entry(
        self,
        file_path: Path,
        object_cid: str,
        collection_name: str,
        user: str,
        msg: str,
    ):
        """Create a log entry."""
        entry = {
            "file": file_path.name,
            "object_cid": object_cid,
            "collection": collection_name,
            "path": str(file_path),
            "user": user,
            "msg": msg,
        }
        print(
            f" File: {entry['file']} -> Collection: {entry['collection']} \n Msg: {entry['msg']}"
        )
        return entry

    def get_filtered_files(
        self, objects: List[FileWithCID], collection_cid: str = None
    ) -> (List[FileWithCID], List[FileWithCID]):  # type: ignore
        """
        Filter files into stamped and not stamped groups based on collection_cid.
        """
        stamped_items = []
        not_stamped_items = []

        if not objects:
            return (not_stamped_items, stamped_items)

        object_cids = [obj.object_cid for obj in objects]
        verification_result = self.stamping_client.verify(object_cids)
        # Build the stamp_dict
        stamp_dict = {
            f"{obj.object_cid}_{obj.collection_hash or 'None'}": obj
            for obj in verification_result.stamp_list
        }

        for obj in objects:
            key = f"{obj.object_cid}_{collection_cid or 'None'}"
            if key in stamp_dict:
                stamped_items.append(obj)
            else:
                not_stamped_items.append(obj)
        return (not_stamped_items, stamped_items)

    # pylint: disable=too-many-locals
    def run(self, current_user: str):
        """Run the processing pipeline for the current user."""
        self.stamped_files = []
        collections = self.data_source.load_collections(current_user)
        for collection in collections:
            collection_path = collection.get("collection_path")
            collection_name = collection.get("collection_name")
            collection_cid = collection.get("collection_cid")
            objects = self.data_source.get_files_for_collection(collection_path)
            objects, _ = self.get_filtered_files(objects, collection_cid=collection_cid)
            # self.move_files_to_archive(exiting_files, collection_path)
            for file_object in objects:
                file_path = file_object.file_path
                object_cid = file_object.object_cid
                with open(file_path, "rb") as f:
                    input_files = {"file": f}
                    data = {
                        "storeStampedFiles": "true",
                        "idempotent": "true",
                    }
                    if collection_cid:
                        data["collectionCid"] = collection_cid
                        msg = f"file {file_path.name} in collection {collection_name} with CID {collection_cid}"
                    else:
                        msg = f"file {file_path.name} without collection CID"

                    entry = self.log_entry(
                        file_path,
                        object_cid,
                        collection_name,
                        current_user,
                        "Start stamping  -" + msg,
                    )
                    self.stamped_files.append(entry)

                    result = self.stamping_client.stamp(
                        input_data=data, input_files=input_files
                    )
                    entry = self.log_entry(
                        file_path,
                        object_cid,
                        collection_name,
                        current_user,
                        "End stamping  -" + json.dumps(result),
                    )
                    self.stamped_files.append(entry)

            self.move_files_to_archive(objects, collection_path)

    def move_files_to_archive(self, files: List[FileWithCID], collection_path: str):
        """
        move files to new archive path
        """
        archive_path = Path(collection_path) / "archive"
        # Create archive folder if it doesn't exist
        archive_path.mkdir(parents=True, exist_ok=True)
        for file_obj in files:
            if file_obj.file_path:
                # Split the filename and extension
                stem = file_obj.file_path.stem  # filename without extension
                suffix = file_obj.file_path.suffix  # extension, like .pdf
                timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
                new_filename = f"{stem}_{timestamp}{suffix}"
                new_path = os.path.join(archive_path, new_filename)
                # Move the file to the archive directory
                shutil.move(file_obj.file_path, new_path)
                print(
                    f"Moved '{file_obj.file_path.name}' to archive: {file_obj.file_path} → {new_path}"
                )
                # Update the file_path if needed
                file_obj.file_path = new_path

    def preview_configuration(self, current_user: str) -> Dict:
        """Preview the configuration for the current user."""
        return {
            "active_user": current_user,
            "collections": self.data_source.load_collections(current_user),
        }

    def write_log(self, path: Path):
        """Write the stamped files log to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.stamped_files, f, indent=2)

    def print_summary(self):
        """Print a summary of the stamped files."""
        print("\n=== Summary of Stamped Files ===")
        for entry in self.stamped_files:
            print(
                f"{entry['file']} -> Collection: {entry['collection']} | Response: {entry['msg']}"
            )
