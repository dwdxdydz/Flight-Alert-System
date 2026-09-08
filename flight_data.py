from dataclasses import dataclass, field



@dataclass(frozen=True)
class FlightData:
    """Normalized flight information returned by the flight search provider."""
    """Normalized flight information."""

    departure_city: str
    departure_airport_code: str
    destination: str
    destination_airport_code: str
    price: float
    outbound_date: str
    return_date: str
    stop_overs: int = 0
    via_cities: list[str] = field(default_factory=list)
    booking_url: str = ""

    def __str__(self) -> str:
        stops = "direct" if self.stop_overs == 0 else f"{self.stop_overs} stop(s)"
        return (
            f"{self.departure_airport_code} → {self.destination_airport_code} "
            f"| €{self.price:.2f} | {stops}"
        )
        return f"{self.departure_airport_code} → {self.destination_airport_code} | €{self.price:.2f} | {stops}"
