"""Flight price alert application entry point."""

import argparse
import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

LOGGER = logging.getLogger(__name__)


def env_int(name: str, default: int) -> int:
    """Read a positive integer environment variable with a useful error."""
    value = os.getenv(name)
    if not value:
        return default
    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer") from error
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


def build_alert(flight: FlightData, target_price: float) -> tuple[str, str]:
    """Build a plain-text notification for a qualifying flight."""
    subject = f"✈️ Flight Deal: €{flight.price:.0f} to {flight.destination}"
    stops = (
        "Direct flight."
        if flight.stop_overs == 0
        else f"{flight.stop_overs} stop(s), via {', '.join(flight.via_cities)}."
    )
    body = (
        "Low-price flight alert!\n\n"
        f"Route: {flight.departure_city} ({flight.departure_airport_code}) → "
        f"{flight.destination} ({flight.destination_airport_code})\n"
        f"Price: €{flight.price:.2f} (target: €{target_price:.2f})\n"
        f"Dates: {flight.outbound_date} → {flight.return_date}\n"
        f"Stops: {stops}\n"
    )
    if flight.booking_url:
        body += f"\nBook/search: {flight.booking_url}\n"
    return subject, body


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search for flights below configured target prices."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print qualifying alerts without sending emails.",
    )
    return parser.parse_args()


def run(dry_run: bool = False) -> None:
    """Run one complete destination scan."""
    load_dotenv()
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    search_weeks = env_int("SEARCH_WEEKS", 26)
    max_stopovers = int(os.getenv("MAX_STOPOVERS", "0"))
    if max_stopovers < 0:
        raise ValueError("MAX_STOPOVERS cannot be negative")

    manager = DataManager(
        os.getenv("SHEETY_ENDPOINT", ""),
        os.getenv("SHEETY_BEARER_TOKEN", ""),
    )
    search = FlightSearch(
        os.getenv("TEQUILA_ENDPOINT", ""),
        os.getenv("TEQUILA_API_KEY", ""),
        origin=os.getenv("ORIGIN_AIRPORT", "AMS"),
    )
    notifier = NotificationManager(
        os.getenv("FROM_EMAIL", ""),
        os.getenv("EMAIL_PASSWORD", ""),
        os.getenv("SMTP_HOST", ""),
        env_int("SMTP_PORT", 587),
    )

    destinations = manager.get_flight_data()
    users = manager.get_users()
    today = datetime.now()
    search_end = today + timedelta(weeks=search_weeks)

    for destination in destinations:
        city = str(destination.get("city", "")).strip()
        code = str(destination.get("iataCode", "")).strip().upper()

        try:
            target = float(destination.get("lowestPrice", 0))
        except (TypeError, ValueError):
            LOGGER.warning("Skipping %s: invalid target price", city or "unknown")
            continue

        if not city or target <= 0:
            LOGGER.warning("Skipping invalid destination row: %s", destination)
            continue

        if not code:
            code = search.get_iata_code(city) or ""
            if not code:
                LOGGER.warning("Skipping %s: IATA code not found", city)
                continue
            if destination.get("id"):
                manager.update_flight_data(destination["id"], code)

        try:
            flight = search.search_flights(code, today, search_end, max_stopovers)
        except Exception:
            LOGGER.exception("Flight search failed for %s (%s)", city, code)
            continue

        if not flight or flight.price > target:
            LOGGER.info("No qualifying deal for %s", city)
            continue

        subject, body = build_alert(flight, target)
        if dry_run:
            LOGGER.info("DRY RUN\n%s\n%s", subject, body)
            continue

        for user in users:
            email = str(user.get("email", "")).strip()
            if not email:
                continue
            try:
                notifier.send_email(subject, body, email)
            except Exception:
                LOGGER.exception("Failed to send alert to %s", email)
                continue
            LOGGER.info("Alert sent to %s: %s", email, flight)


if __name__ == "__main__":
    args = parse_args()
    run(dry_run=args.dry_run)
