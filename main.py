import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def build_alert(flight, target_price: float) -> tuple[str, str]:
    subject = f"✈️ Flight Deal: €{flight.price:.0f} to {flight.destination}"
    stops = (
        "Direct flight."
        if flight.stop_overs == 0
        else f"{flight.stop_overs} stop(s), via {', '.join(flight.via_cities)}."
    )
    body = (
        f"Low-price flight alert!\n\n"
        f"Route: {flight.departure_city} ({flight.departure_airport_code}) → "
        f"{flight.destination} ({flight.destination_airport_code})\n"
        f"Price: €{flight.price:.2f} (target: €{target_price:.2f})\n"
        f"Dates: {flight.outbound_date} → {flight.return_date}\n"
        f"Stops: {stops}\n"
    )
    if flight.booking_url:
        body += f"\nBook/search: {flight.booking_url}\n"
    return subject, body


def run() -> None:
    load_dotenv()

    data_manager = DataManager(
        os.getenv("SHEETY_ENDPOINT", ""),
        os.getenv("SHEETY_BEARER_TOKEN", ""),
    )
    flight_search = FlightSearch(
        os.getenv("TEQUILA_ENDPOINT", ""),
        os.getenv("TEQUILA_API_KEY", ""),
    )
    notifier = NotificationManager(
        os.getenv("FROM_EMAIL", ""),
        os.getenv("EMAIL_PASSWORD", ""),
        os.getenv("SMTP_HOST", ""),
        env_int("SMTP_PORT", 587),
    )

    origin = os.getenv("ORIGIN_AIRPORT", "AMS")
    search_weeks = env_int("SEARCH_WEEKS", 26)
    min_nights = env_int("MIN_NIGHTS", 7)
    max_nights = env_int("MAX_NIGHTS", 28)
    max_stops = env_int("MAX_STOPOVERS", 0)

    # FlightSearch currently uses its configured origin internally.
    _ = origin, min_nights, max_nights

    destinations = data_manager.get_flight_data()
    users = data_manager.get_users()
    today = datetime.now()

    for destination in destinations:
        city = str(destination.get("city", "")).strip()
        iata_code = str(destination.get("iataCode", "")).strip()
        target_price = float(destination.get("lowestPrice", 0))

        if not iata_code:
            iata_code = flight_search.get_iata_code(city)
            if not iata_code:
                print(f"Skipping {city}: IATA code not found.")
                continue
            if destination.get("id"):
                data_manager.update_flight_data(destination["id"], iata_code)

        flight = flight_search.search_flights(
            iata_code,
            today,
            today + timedelta(weeks=search_weeks),
            max_stops=max_stops,
        )

        if flight and flight.price <= target_price:
            subject, body = build_alert(flight, target_price)
            for user in users:
                email = user.get("email")
                if email:
                    notifier.send_email(subject, body, email)
                    print(f"Alert sent to {email}: {flight}")


if __name__ == "__main__":
    run()
