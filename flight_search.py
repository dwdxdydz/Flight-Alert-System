from datetime import datetime
from typing import Any, Dict, Optional

import requests

from flight_data import FlightData


class FlightSearch:
    """Search and normalize flight data from a Tequila-compatible API."""

    def __init__(self, endpoint: str, api_key: str, timeout: int = 20):
        if not endpoint:
            raise ValueError("TEQUILA_ENDPOINT is required")
        if not api_key:
            raise ValueError("TEQUILA_API_KEY is required")

        self.endpoint = endpoint.rstrip("/")
        self.headers = {"apikey": api_key}
        self.timeout = timeout

    def get_iata_code(self, city: str) -> Optional[str]:
        if not city:
            return None

        response = requests.get(
            f"{self.endpoint}/locations/query",
            headers=self.headers,
            params={"term": city, "location_types": "airport"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        locations = response.json().get("locations", [])

        for location in locations:
            code = location.get("code")
            if code:
                return code
        return None

    def search_flights(
        self,
        destination: str,
        date_from: datetime,
        date_to: datetime,
        max_stops: int = 0,
    ) -> Optional[FlightData]:
        if not destination:
            return None

        params = {
            "fly_from": "AMS",
            "fly_to": destination,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "max_stopovers": max_stops,
            "curr": "EUR",
            "one_for_city": 1,
            "sort": "price",
        }

        result = self._request_search(params)
        flight = self._parse_flight_data(result)

        if flight is None and max_stops == 0:
            params["max_stopovers"] = 2
            flight = self._parse_flight_data(self._request_search(params))

        return flight

    def _request_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.get(
            f"{self.endpoint}/v2/search",
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _parse_flight_data(result: Dict[str, Any]) -> Optional[FlightData]:
        flights = result.get("data", [])
        if not flights:
            return None

        data = flights[0]
        route = data.get("route", [])
        if not route:
            return None

        via_cities = [
            segment.get("cityTo", "")
            for segment in route[:-1]
            if segment.get("cityTo")
        ]

        booking_url = data.get("deep_link", "")

        return FlightData(
            departure_city=data.get("cityFrom", ""),
            departure_airport_code=data.get("flyFrom", ""),
            destination=data.get("cityTo", ""),
            destination_airport_code=data.get("flyTo", ""),
            price=float(data.get("price", 0)),
            outbound_date=route[0].get("local_departure", "")[:10],
            return_date=route[-1].get("local_departure", "")[:10],
            stop_overs=max(0, len(route) - 1),
            via_cities=via_cities,
            booking_url=booking_url,
        )
