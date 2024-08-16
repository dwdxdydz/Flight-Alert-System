import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Load environment variables from .env file
load_dotenv()

# Initialize Data Manager
data_manager = DataManager(os.getenv('SHEETY_ENDPOINT'), os.getenv('SHEETY_BEARER_TOKEN'))

# Fetch flight data and users from Google Sheets
flight_data = data_manager.get_flight_data()
users = data_manager.get_users()

# Initialize Flight Search and Notification Manager
flight_search = FlightSearch(os.getenv('TEQUILA_ENDPOINT'), os.getenv('TEQUILA_API_KEY'))
notification_manager = NotificationManager(
    from_email=os.getenv('FROM_EMAIL'),
    password=os.getenv('EMAIL_PASSWORD'),
    smtp=os.getenv('SMTP')
)

# Process each flight entry
for entry in flight_data:
    # Add missing IATA codes for destinations
    if not entry['iataCode']:
        entry['iataCode'] = flight_search.get_iata_code({"term": entry['city']})
        data_manager.update_flight_data(entry['id'], entry)

    # Search flights for each destination
    flight = flight_search.search_flights(
        destination=entry['iataCode'],
        date_from=datetime.now(),
        date_to=datetime.now() + timedelta(weeks=26),
        max_stops=0
    )

    # Send email to users if flight price is less than or equal to the lowest price
    if flight and flight.price <= entry['lowestPrice']:
        google_flight_link = (
            f"https://www.google.co.uk/flights/?hl=en#flt={flight.departure_airport_code}."
            f"{flight.destination_airport_code}.{flight.outbound_date}*"
            f"{flight.destination_airport_code}.{flight.departure_airport_code}.{flight.return_date}"
        )

        email_msg = (
            f"Subject: Low price alert!\n\n"
            f"Low price alert! Only {flight.price} Euro to fly from "
            f"{flight.departure_city}-{flight.departure_airport_code} to "
            f"{flight.destination}-{flight.destination_airport_code}, from "
            f"{flight.outbound_date} to {flight.return_date}.\n"
        )

        # Add details about stopovers
        if flight.stop_overs == 0:
            email_msg += "Direct flight.\n"
        elif flight.stop_overs == 1:
            email_msg += f"Flight with 1 stopover, via {flight.via_cities[0]}.\n"
        else:
            email_msg += (
           
