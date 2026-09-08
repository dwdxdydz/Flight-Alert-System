from typing import Any

import requests


class DataManager:
    """Client for the configured Sheety-style data API."""

    def __init__(self, endpoint: str, token: str, timeout: int = 15):
        if not endpoint or not token:
            raise ValueError("SHEETY_ENDPOINT and SHEETY_BEARER_TOKEN are required")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.endpoint = endpoint.rstrip("/")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.timeout = timeout

    def _request(
        self, method: str, path: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        response = requests.request(
            method,
            f"{self.endpoint}/{path.lstrip('/')}",
            headers=self.headers,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Data API response must be a JSON object")
        return data

    def get_flight_data(self) -> list[dict[str, Any]]:
        prices = self._request("GET", "prices").get("prices", [])
        if not isinstance(prices, list):
            raise ValueError("Data API 'prices' field must be a list")
        return [price for price in prices if isinstance(price, dict)]

    def update_flight_data(self, row_id: Any, iata_code: str) -> dict[str, Any]:
        return self._request("PUT", f"prices/{row_id}", {"price": {"iataCode": iata_code}})

    def get_users(self) -> list[dict[str, Any]]:
        users = self._request("GET", "users").get("users", [])
        if not isinstance(users, list):
            raise ValueError("Data API 'users' field must be a list")
        return [user for user in users if isinstance(user, dict)]

    def add_user(self, first_name: str, last_name: str, email: str) -> dict[str, Any]:
        return self._request(
            "POST",
            "users",
            {"user": {"firstName": first_name, "lastName": last_name, "email": email}},
        )
