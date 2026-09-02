from typing import Any, Dict, List, Optional
import requests

class DataManager:
    """Client for the configured Sheety-style data API."""
    def __init__(self, endpoint: str, token: str, timeout: int = 15):
        if not endpoint or not token:
            raise ValueError("SHEETY_ENDPOINT and SHEETY_BEARER_TOKEN are required")
        self.endpoint = endpoint.rstrip("/")
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        self.timeout = timeout

    def _request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.request(method, f"{self.endpoint}/{path.lstrip('/')}", headers=self.headers, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_flight_data(self) -> List[Dict[str, Any]]:
        return self._request("GET", "prices").get("prices", [])

    def update_flight_data(self, row_id: Any, iata_code: str) -> Dict[str, Any]:
        return self._request("PUT", f"prices/{row_id}", {"price": {"iataCode": iata_code}})

    def get_users(self) -> List[Dict[str, Any]]:
        return self._request("GET", "users").get("users", [])

    def add_user(self, first_name: str, last_name: str, email: str) -> Dict[str, Any]:
        return self._request("POST", "users", {"user": {"firstName": first_name, "lastName": last_name, "email": email}})
