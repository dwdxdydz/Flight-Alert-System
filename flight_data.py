from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class FlightData:
    """Normalized flight information."""
    departure_city: str
    departure_airport_code: str
    destination: str
    destination_airport_code: str
    price: float
    outbound_date: str
    return_date: str
    stop_overs: int = 0
    via_cities: List[str] = field(default_factory=list)
    booking_url: str = ""

    def __str__(self) -> str:
        stops = "direct" if self.stop_overs == 0 else f"{self.stop_overs} stop(s)"
        return f"{self.departure_airport_code} → {self.destination_airport_code} | €{self.price:.2f} | {stops}
