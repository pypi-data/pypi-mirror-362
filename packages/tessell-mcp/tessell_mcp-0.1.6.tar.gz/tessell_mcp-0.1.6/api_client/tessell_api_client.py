"""
Tessell API Client

This module provides a simple client for interacting with the Tessell API using the required configuration.
"""

from typing import Optional
import httpx
import time

class TessellApiClient:
    """Client for interacting with the Tessell API, with access token caching or direct JWT usage."""
    def __init__(self, base_url: str, tenant_id: str, api_key: Optional[str] = None, jwt_token: Optional[str] = None, timeout: Optional[float] = 10.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.jwt_token = jwt_token
        self.tenant_id = tenant_id
        self.timeout = timeout
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)
        self._token_cache = {}

    def __get_access_token(self) -> str:
        """Fetches the Tessell access token from the API or cache, unless jwt_token is already provided."""
        if self.jwt_token:
            return self.jwt_token
        current_time = time.time()
        if "access_token" in self._token_cache and self._token_cache["expiry_time"] > current_time:
            return self._token_cache["access_token"]
        url = f"{self.base_url}/iam/authorize"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "tenant-id": self.tenant_id
        }
        payload = {
            "apiKey": self.api_key
        }
        response = self._client.post(url.replace(self.base_url, ""), headers=headers, json=payload)
        response.raise_for_status()
        access_token = response.json()["accessToken"]
        # Cache the token with an expiry time of 58 minutes
        self._token_cache["access_token"] = access_token
        self._token_cache["expiry_time"] = time.time() + 58 * 60
        return access_token

    def get_headers(self) -> dict:
        """Get headers for Tessell API requests, using either a provided JWT or a fetched access token."""
        return {
            "Authorization": f"{self.__get_access_token()}",
            "Tenant-ID": self.tenant_id,
            "Content-Type": "application/json",
        }

    def _get(self, path: str, **kwargs):
        """[INTERNAL] Send a GET request to the Tessell API. Use only within this client."""
        headers = self.get_headers()
        return self._client.get(path, headers=headers, **kwargs)

    def _post(self, path: str, json: dict = None, **kwargs):
        """[INTERNAL] Send a POST request to the Tessell API. Use only within this client."""
        headers = self.get_headers()
        return self._client.post(path, json=json, headers=headers, **kwargs)

    def _patch(self, path: str, json: dict = None, **kwargs):
        """[INTERNAL] Send a PATCH request to the Tessell API. Use only within this client."""
        headers = self.get_headers()
        return self._client.patch(path, json=json, headers=headers, **kwargs)

    def get_service_details(self, service_id: str):
        """
        Fetch details for a specific service by service_id.
        """
        resp = self._get(f"/services/{service_id}")
        return resp

    def get_services(self, page_size: int = 10, name: str = None):
        """
        Fetch a list of services from the Tessell API. Optionally filter by service name.
        """
        params = {"page-size": page_size}
        if name:
            params["name"] = name
        resp = self._get("/services", params=params)
        return resp

    def start_service(self, service_id: str, comment: str = ""):
        """
        Start a database service by service_id, with optional comment payload.
        """
        payload = {"comment": comment}
        return self._patch(f"/services/{service_id}/start", json=payload)

    def stop_service(self, service_id: str, start_after_hours: int = 24, comment: str = ""):
        """
        Stop a database service by service_id, with optional startAfterHours and comment payload.
        """
        payload = {"startAfterHours": start_after_hours, "comment": comment}
        return self._patch(f"/services/{service_id}/stop", json=payload)

    def create_snapshot(self, availability_machine_id: str, name: str, description: str = "") -> dict:
        """
        Create a new snapshot for a specific availability machine.

        Args:
            availability_machine_id (str): The ID of the availability machine.
            name (str): The name of the snapshot.
            description (str, optional): The description of the snapshot.

        Returns:
            dict: The details of the created snapshot.
        """
        payload = {
            "name": name,
            "description": description
        }
        resp = self._post(f"/availability-machines/{availability_machine_id}/snapshots", json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_availability_machine_snapshots(self, availability_machine_id: str):
        """
        Fetch all snapshots for a specific availability machine.
        """
        resp = self._get(f"/availability-machines/{availability_machine_id}/snapshots")
        return resp

    def close(self):
        self._client.close()