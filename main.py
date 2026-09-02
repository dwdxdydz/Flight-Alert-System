import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default

def build_alert(flight, target_price: float):
    subject = f"✈️ Flight Deal: €{flight.price:.0f} to {flight.destination}"
    stops = "Direct flight." if flight.stop_overs == 0 else f"{flight.stop_overs} stop(s), via {', '.join(flight.via_cities)}."
    body = (f"Low-price flight alert!\n\nRoute: {flight.departure_city} ({flight.departure_airport_code}) → {flight.destination} ({flight.destination_airport_code})\nPrice: €{flight.price:.2f} (target: €{target_price:.2f})\nDates: {flight.outbound_date} → {flight.return_date}\nStops: {stops}\n")
    if flight.booking_url: body += f"\nBook/search: {flight.booking_url}\n"
    return subject, body

def run() -> None:
    load_dotenv()
    manager = DataManager(os.getenv("SHEETY_ENDPOINT",""), os.getenv("SHEETY_BEARER_TOKEN",""))
    search = FlightSearch(os.getenv("TEQUILA_ENDPOINT",""), os.getenv("TEQUILA_API_KEY",""), origin=os.getenv("ORIGIN_AIRPORT","AMS"))
    notifier = NotificationManager(os.getenv("FROM_EMAIL",""), os.getenv("EMAIL_PASSWORD",""), os.getenv("SMTP_HOST",""), env_int("SMTP_PORT",587))
    destinations, users = manager.get_flight_data(), manager.get_users()
    today = datetime.now()
    for destination in destinations:
        city, code = str(destination.get("city","")).strip(), str(destination.get("iataCode","")).strip()
        target = float(destination.get("lowestPrice",0))
        if not code:
            code = search.get_iata_code(city)
            if not code: print(f"Skipping {city}: IATA code not found."); continue
            if destination.get("id"): manager.update_flight_data(destination["id"], code)
        flight = search.search_flights(code, today, today + timedelta(weeks=env_int("SEARCH_WEEKS",26)), env_int("MAX_STOPOVERS",0))
        if flight and flight.price <= target:
            subject, body = build_alert(flight, target)
            for user in users:
                if user.get("email"):
                    notifier.send_email(subject, body, user["email"])
                    print(f"Alert sent to {user['email']}: {flight}")

if __name__ == "__main__":
    run()
