from datetime import datetime
import math
from typing import Any

import requests

from flight_data import FlightData


class FlightSearch:
    """Search and normalize flight data from a Tequila-compatible API."""

    def __init__(
        self, endpoint: str, api_key: str, origin: str = "AMS", timeout: int = 20
    ) -> None:
        if not endpoint or not api_key:
            raise ValueError("TEQUILA_ENDPOINT and TEQUILA_API_KEY are required")
        if timeout <= 0:
            raise ValueError("timeout must be positive")

        self.endpoint = endpoint.rstrip("/")
        self.origin = origin.strip().upper()
        self.timeout = timeout
        self.headers = {"apikey": api_key}

    def get_iata_code(self, city: str) -> str | None:
        """Return the first airport IATA code matching *city*, if one is available."""
        if not city.strip():
            return None

        response = requests.get(
            f"{self.endpoint}/locations/query",
            headers=self.headers,
            params={"term": city, "location_types": "airport"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        for location in response.json().get("locations", []):
            code = location.get("code")
            if code:
                return str(code).upper()
        return None

    def search_flights(
        self,
        destination: str,
        date_from: datetime,
        date_to: datetime,
        max_stops: int = 0,
    ) -> FlightData | None:
        """Find the cheapest trip, retrying with connections for direct-only searches."""
        destination = destination.strip().upper()
        if not destination:
            raise ValueError("destination is required")
        if max_stops < 0:
            raise ValueError("max_stops cannot be negative")
        if date_to < date_from:
            raise ValueError("date_to cannot be before date_from")

        params = {
            "fly_from": self.origin,
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
        flight = self._parse_flight_data(self._request_search(params))
        if flight is None and max_stops == 0:
            params["max_stopovers"] = 2
            flight = self._parse_flight_data(self._request_search(params))
        return flight

    def _request_search(self, params: dict[str, Any]) -> dict[str, Any]:
        response = requests.get(
            f"{self.endpoint}/v2/search",
            headers=self.headers,
            params=params,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _parse_flight_data(result: dict[str, Any]) -> FlightData | None:
        """Convert the provider response's first valid itinerary into ``FlightData``."""
        if not isinstance(result, dict):
            return None

        flights = result.get("data", [])
        if not isinstance(flights, list):
            return None

        for data in flights:
            if not isinstance(data, dict):
                continue
            route = data.get("route", [])
            if not isinstance(route, list) or not route:
                continue

            try:
                price = float(data["price"])
            except (KeyError, TypeError, ValueError):
                continue
            if not math.isfinite(price) or price < 0:
                continue

            segments = [segment for segment in route if isinstance(segment, dict)]
            if not segments:
                continue

            # Kiwi returns both the outbound and inbound legs in ``route``.  A
            # direct return trip therefore has two segments, not one stop.
            def is_return_segment(segment: dict[str, Any]) -> bool:
                return str(segment.get("return", "0")) == "1"

            outbound_segments = [
                segment for segment in segments if not is_return_segment(segment)
            ]
            if not outbound_segments:
                outbound_segments = segments
            inbound_segments = [segment for segment in segments if is_return_segment(segment)]
            first_segment = outbound_segments[0]
            return_segment = inbound_segments[0] if inbound_segments else segments[-1]

            return FlightData(
                departure_city=str(data.get("cityFrom", "")),
                departure_airport_code=str(data.get("flyFrom", "")),
                destination=str(data.get("cityTo", "")),
                destination_airport_code=str(data.get("flyTo", "")),
                price=price,
                outbound_date=str(first_segment.get("local_departure", ""))[:10],
                return_date=str(return_segment.get("local_departure", ""))[:10],
                stop_overs=max(0, len(outbound_segments) - 1),
                via_cities=[
                    str(segment["cityTo"])
                    for segment in outbound_segments[:-1]
                    if segment.get("cityTo")
                ],
                booking_url=str(data.get("deep_link", "")),
            )
        return None
