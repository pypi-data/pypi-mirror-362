"""Stamping Service for VBase API"""

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypedDict

import requests

logger = logging.getLogger(__name__)
REQUEST_TIMEOUT = 30


@dataclass
# pylint: disable=too-many-instance-attributes
class StampVerification:
    """Data structure for a single stamp verification."""

    chain_id: Optional[int]
    transaction_hash: Optional[str]
    user: Optional[str]
    object_cid: str
    collection_hash: Optional[str]
    collection_name: Optional[str]
    timestamp: Optional[str]
    set_cid: Optional[str]
    verified: bool
    verified_since: Optional[str]
    user_id: Optional[str]
    timedelta: Optional[str]
    time: Optional[str]
    block_explorer_url: Optional[str]
    blockchain_name: Optional[str]


@dataclass
class StampVerificationResult:
    """Data structure for the result of a stamp verification."""

    display_timezone: Optional[str]
    stamp_list: List[StampVerification]
    message: Optional[str]


class StampData(TypedDict, total=False):
    """Data structure for the stamping API request payload.

    Naming convention:
    - 'dataCid' refers to the CID (Content Identifier) of the input data.
    - 'collectionCid' refers to the CID of the associated collection.
    """

    data: Optional[str]
    dataCid: Optional[str]
    collectionCid: Optional[str]
    storeStampedFiles: bool
    idempotent: bool
    idempotencyWindow: int


class ApiClient:
    """Api Client for interacting with the VBase API for stamping files."""

    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.stamp_url = f"{self.base_url}/api/v1/stamp/"
        self.verify_url = f"{self.base_url}/api/v1/verify/"
        self.collection_url = f"{self.base_url}/api/v1/collection/"
        self.user_url = f"{self.base_url}/api/v1/user/"

    def stamp(
        self,
        input_data: Optional[StampData] = None,
        input_files: Optional[Dict[str, Any]] = None,
    ) -> Dict:
        """Send a stamping request to the VBase API."""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        if input_files is None:
            input_files = {}

        try:
            response = requests.post(
                self.stamp_url,
                data=input_data,
                files=input_files,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Request to VBase API failed: %s", e)
            logger.error(
                "Response: %s",
                response.text if "response" in locals() else "No response",
            )

            curl_cmd = self._build_curl(
                self.stamp_url, headers, input_data, input_files
            )
            logger.error("Try this with curl:\n%s", curl_cmd)
            raise

        try:
            return response.json()
        except Exception as e:
            logger.error("Failed to parse JSON from stamp response: %s", response.text)
            raise e

    def verify(self, object_hashes: List[str]) -> StampVerificationResult:
        """Send a verification request to the VBase API and parse the result into dataclasses."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "object-hashes": object_hashes,
            "filter-by-user": True,
        }

        try:
            response = requests.post(
                self.verify_url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Verification request failed: %s", e)
            logger.error(
                "Response: %s",
                response.text if "response" in locals() else "No response",
            )
            curl_cmd = self._build_curl_json(self.verify_url, headers, payload)
            logger.error("Try this with curl:\n%s", curl_cmd)
            raise

        try:
            data = response.json()
            stamp_list_data = data.get("stamp_list") or []
            stamp_list = []
            if len(stamp_list_data) > 0:
                for entry in stamp_list_data:
                    stamp = StampVerification(
                        chain_id=entry.get("chainId"),
                        transaction_hash=entry.get("transactionHash"),
                        user=entry.get("user"),
                        object_cid=entry["objectCid"],  # required
                        timestamp=entry.get("timestamp"),
                        set_cid=entry.get("setCid"),
                        verified=entry.get("verified", False),
                        verified_since=entry.get("verified_since"),
                        user_id=entry.get("user_id"),
                        timedelta=entry.get("timedelta"),
                        time=entry.get("time"),
                        collection_hash=entry.get("collection_hash"),
                        collection_name=entry.get("collection_name"),
                        block_explorer_url=entry.get("blockExplorerUrl"),
                        blockchain_name=entry.get("blockchainName"),
                    )
                    stamp_list.append(stamp)

            return StampVerificationResult(
                display_timezone=data.get("display_timezone"),
                stamp_list=stamp_list,
                message=data.get("message"),
            )

        except Exception as e:
            logger.error("Failed to parse verification response: %s", response.text)
            raise RuntimeError("Invalid verification response") from e

    def fetch_collections(self) -> Dict:
        """Fetch the list of collections available to the current user."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json",
        }

        try:
            response = requests.get(
                self.collection_url, headers=headers, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Fetching collections failed: %s", e)
            logger.error(
                "Response: %s",
                response.text if "response" in locals() else "No response",
            )
            curl_cmd = self._build_curl_get(self.collection_url, headers)
            logger.error("Try this with curl:\n%s", curl_cmd)
            raise

        try:
            return response.json()
        except Exception as e:
            logger.error(
                "Failed to parse JSON from collections response: %s", response.text
            )
            raise e

    def fetch_user_profile(self) -> Dict:
        """Fetch details of the currently authenticated user."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json",
        }

        try:
            response = requests.get(
                self.user_url, headers=headers, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Fetching user profile failed: %s", e)
            logger.error(
                "Response: %s",
                response.text if "response" in locals() else "No response",
            )
            curl_cmd = self._build_curl_get(self.user_url, headers)
            logger.error("Try this with curl:\n%s", curl_cmd)
            raise

        try:
            return response.json()
        except Exception as e:
            logger.error(
                "Failed to parse JSON from user profile response: %s", response.text
            )
            raise e

    def _build_curl(self, url: str, headers: dict, data: dict, files: dict) -> str:
        """Build a curl command for the given request parameters."""
        curl_parts = [f"curl -X POST '{url}'"]

        # Add headers
        for k, v in headers.items():
            curl_parts.append(f"-H '{k}: {v}'")

        # Add form fields
        for k, v in data.items():
            curl_parts.append(f"-F '{k}={v}'")

        # Add files
        for k, file_value in files.items():
            if isinstance(file_value, tuple):
                # format: (filename, fileobj, ...)
                filename = file_value[0]
            elif hasattr(file_value, "name"):
                # file object directly
                filename = file_value.name
            else:
                filename = "unknown"

            curl_parts.append(f"-F '{k}=@{filename}'")

        return " \\\n  ".join(curl_parts)

    def _build_curl_json(self, url: str, headers: dict, json_data: dict) -> str:
        """Build a curl command for a JSON POST request."""
        curl_parts = [f"curl -X POST '{url}'"]

        for k, v in headers.items():
            curl_parts.append(f"-H '{k}: {v}'")

        curl_parts.append(f"-d '{json.dumps(json_data)}'")

        return " \\\n  ".join(curl_parts)

    def _build_curl_get(self, url: str, headers: dict) -> str:
        """Build a curl command for a GET request."""
        curl_parts = [f"curl -X GET '{url}'"]
        for k, v in headers.items():
            curl_parts.append(f"-H '{k}: {v}'")
        return " \\\n  ".join(curl_parts)
