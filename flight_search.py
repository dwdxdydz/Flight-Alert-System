from datetime import datetime
from typing import Any, Dict, Optional
import requests
from flight_data import FlightData

class FlightSearch:
    """Search and normalize flight data from a Tequila-compatible API."""
    def __init__(self, endpoint: str, api_key: str, origin: str = "AMS", timeout: int = 20):
        if not endpoint or not api_key:
            raise ValueError("TEQUILA_ENDPOINT and TEQUILA_API_KEY are required")
        self.endpoint, self.origin, self.timeout = endpoint.rstrip("/"), origin, timeout
        self.headers = {"apikey": api_key}

    def get_iata_code(self, city: str) -> Optional[str]:
        if not city: return None
        response = requests.get(f"{self.endpoint}/locations/query", headers=self.headers, params={"term": city, "location_types": "airport"}, timeout=self.timeout)
        response.raise_for_status()
        for location in response.json().get("locations", []):
            if location.get("code"): return location["code"]
        return None

    def search_flights(self, destination: str, date_from: datetime, date_to: datetime, max_stops: int = 0) -> Optional[FlightData]:
        params = {"fly_from": self.origin, "fly_to": destination, "date_from": date_from.strftime("%d/%m/%Y"), "date_to": date_to.strftime("%d/%m/%Y"), "nights_in_dst_from": 7, "nights_in_dst_to": 28, "max_stopovers": max_stops, "curr": "EUR", "one_for_city": 1, "sort": "price"}
        flight = self._parse_flight_data(self._request_search(params))
        if flight is None and max_stops == 0:
            params["max_stopovers"] = 2
            flight = self._parse_flight_data(self._request_search(params))
        return flight

    def _request_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.get(f"{self.endpoint}/v2/search", headers=self.headers, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _parse_flight_data(result: Dict[str, Any]) -> Optional[FlightData]:
        flights = result.get("data", [])
        if not flights: return None
        data, route = flights[0], flights[0].get("route", [])
        if not route: return None
        return FlightData(
            departure_city=data.get("cityFrom", ""), departure_airport_code=data.get("flyFrom", ""),
            destination=data.get("cityTo", ""), destination_airport_code=data.get("flyTo", ""),
            price=float(data.get("price", 0)), outbound_date=route[0].get("local_departure", "")[:10],
            return_date=route[-1].get("local_departure", "")[:10], stop_overs=max(0, len(route)-1),
            via_cities=[s.get("cityTo","") for s in route[:-1] if s.get("cityTo")],
            booking_url=data.get("deep_link", "")
        )
