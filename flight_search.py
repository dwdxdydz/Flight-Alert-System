import requests
from flight_data import FlightData
from datetime import datetime

class FlightSearch:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self.headers = {
            "apiKey": self.api_key
        }

    def get_iata_code(self, city: str) -> str:
        """Retrieve the IATA code for a given city."""
        response = requests.get(url=f"{self.endpoint}/locations/query", headers=self.headers, params={"term": city})
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        try:
            iata = result['locations'][0]['code']
        except (IndexError, KeyError):
            print(f"No IATA code found for city: {city}")
            return None
        return iata

    def search_flights(self, destination: str, date_from: datetime, date_to: datetime, max_stops: int) -> FlightData:
        """Search for flights to the specified destination within given dates and max stops."""
        params = {
            "fly_from": "AMS",
            "fly_to": destination,
            "date_from": date_from.strftime('%d/%m/%Y'),
            "date_to": date_to.strftime('%d/%m/%Y'),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "max_stopovers": max_stops,
            "curr": "EUR",
            "one_for_city": 1
        }

        def fetch_flight_data(params):
            """Fetch flight data from the API."""
            response = requests.get(url=f"{self.endpoint}/v2/search", headers=self.headers, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()

        result = fetch_flight_data(params)
        flight_data = self._parse_flight_data(result)

        if flight_data is None:
            # Try with max_stopovers set to 2 if no flights found
            params["max_stopovers"] = 2
            result = fetch_flight_data(params)
            flight_data = self._parse_flight_data(result)

        if flight_data:
            print(f"{flight_data.destination}: €{flight_data.price}, via {flight_data.via_cities}")
            return flight_data
        else:
            print(f"No flights found for {destination}.")
            return None

    def _parse_flight_data(self, result) -> FlightData:
        """Parse flight data from API result into a FlightData object."""
        try:
            data = result['data'][0]
        except (IndexError, KeyError):
            return None

        stop_overs = 0
        via_cities = []
        outbound_date = data['route'][0]['local_departure'].split("T")[0]
        return_date = data['route'][-1]['local_departure'].split("T")[0]

        for route in data['route']:
            if route['flyTo'] != 'AMS' and route['cityCodeTo'] != data['cityTo']:
                via_cities.append(route['cityTo'])
                stop_overs += 1

        return FlightData(
            departure_city=data['cityFrom'],
            dep_code=data['flyFrom'],
            destination=data['cityTo'],
            dest_code=data['flyTo'],
            price=data['price'],
       
