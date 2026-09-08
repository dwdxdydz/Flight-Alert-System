from flight_search import FlightSearch


def test_parse_direct_flight():
    result = {
        "data": [{"cityFrom": "Amsterdam", "flyFrom": "AMS", "cityTo": "Paris", "flyTo": "CDG", "price": 89, "route": [{"cityTo": "Paris", "local_departure": "2026-10-10T08:00:00"}]}]
    }
    flight = FlightSearch._parse_flight_data(result)
    assert flight.destination_airport_code == "CDG"
    assert flight.price == 89
    assert flight.stop_overs == 0

def test_parse_connecting_flight():
    result = {
        "data": [{"cityFrom": "Amsterdam", "flyFrom": "AMS", "cityTo": "Tokyo", "flyTo": "NRT", "price": 500, "route": [{"cityTo": "Doha", "local_departure": "2026-11-10T08:00:00"}, {"cityTo": "Tokyo", "local_departure": "2026-11-10T16:00:00"}]}]
    }
    flight = FlightSearch._parse_flight_data(result)
    assert flight.stop_overs == 1
    assert flight.via_cities == ["Doha"]


def test_parse_return_route_counts_only_outbound_stopovers():
    result = {
        "data": [
            {
                "cityFrom": "Amsterdam",
                "flyFrom": "AMS",
                "cityTo": "Paris",
                "flyTo": "CDG",
                "price": 89,
                "route": [
                    {
                        "cityTo": "Paris",
                        "local_departure": "2026-10-10T08:00:00",
                        "return": 0,
                    },
                    {
                        "cityTo": "Amsterdam",
                        "local_departure": "2026-10-17T12:00:00",
                        "return": 1,
                    },
                ],
            }
        ]
    }

    flight = FlightSearch._parse_flight_data(result)

    assert flight is not None
    assert flight.stop_overs == 0
    assert flight.return_date == "2026-10-17"


def test_parse_skips_non_finite_price():
    result = {"data": [{"price": "NaN", "route": [{}]}]}

    assert FlightSearch._parse_flight_data(result) is None


def test_parse_empty_result():
    assert FlightSearch._parse_flight_data({"data":[]}) is None


def test_parse_skips_malformed_results_before_valid_flight():
    result = {
        "data": [
            {"price": "not-a-price", "route": [{}]},
            {
                "cityFrom": "Amsterdam",
                "flyFrom": "AMS",
                "cityTo": "Paris",
                "flyTo": "CDG",
                "price": "89.50",
                "route": [{"cityTo": "Paris", "local_departure": "2026-10-10T08:00:00"}],
            },
        ]
    }

    flight = FlightSearch._parse_flight_data(result)

    assert flight is not None
    assert flight.price == 89.5
