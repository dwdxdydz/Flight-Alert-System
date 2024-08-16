class FlightData:
    def __init__(self, departure_city, dep_code, destination, dest_code, price, outbound_date, return_date, stop_overs=0, via_cities=None):
        self.departure_city = departure_city
        self.departure_airport_code = dep_code
        self.destination = destination
        self.destination_airport_code = dest_code
        self.price = price
        self.outbound_date = outbound_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        # Use an empty list if via_cities is None
        self.via_cities = via_cities if via_cities is not None else []

    def __repr__(self):
        return (f"FlightData(departure_city={self.departure_city!r}, "
                f"dep_code={self.departure_airport_code!r}, "
                f"destination={self.destination!r}, "
                f"dest_code={self.destination_airport_code!r}, "
                f"price={self.price!r}, "
                f"outbound_date={self.outbound_date!r}, "
                f"return_date={self.return_date!r}, "
                f"stop_overs={self.stop_overs!r}, "
                f"via_cities={self.via_cities!r})")
