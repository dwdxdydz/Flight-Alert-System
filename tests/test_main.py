import pytest

from flight_data import FlightData
from main import build_alert, env_int, env_nonnegative_int


def test_build_alert_includes_booking_link_and_connection_details():
    flight = FlightData(
        departure_city="Amsterdam",
        departure_airport_code="AMS",
        destination="Tokyo",
        destination_airport_code="NRT",
        price=499.99,
        outbound_date="2026-10-10",
        return_date="2026-10-20",
        stop_overs=1,
        via_cities=["Doha"],
        booking_url="https://example.com/book",
    )

    subject, body = build_alert(flight, 500)

    assert subject == "✈️ Flight Deal: €500 to Tokyo"
    assert "1 stop(s), via Doha." in body
    assert "https://example.com/book" in body


def test_env_int_returns_default_for_unset_variable(monkeypatch):
    monkeypatch.delenv("SEARCH_WEEKS", raising=False)

    assert env_int("SEARCH_WEEKS", 26) == 26


def test_env_int_rejects_invalid_value(monkeypatch):
    monkeypatch.setenv("SEARCH_WEEKS", "six months")

    with pytest.raises(ValueError, match="SEARCH_WEEKS must be an integer"):
        env_int("SEARCH_WEEKS", 26)


def test_env_nonnegative_int_allows_zero_and_rejects_negative(monkeypatch):
    monkeypatch.setenv("MAX_STOPOVERS", "0")
    assert env_nonnegative_int("MAX_STOPOVERS", 0) == 0

    monkeypatch.setenv("MAX_STOPOVERS", "-1")
    with pytest.raises(ValueError, match="MAX_STOPOVERS cannot be negative"):
        env_nonnegative_int("MAX_STOPOVERS", 0)
