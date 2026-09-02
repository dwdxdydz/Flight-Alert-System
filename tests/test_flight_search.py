from flight_search import FlightSearch

def test_parse_direct_flight():
    result={"data":[{"cityFrom":"Amsterdam","flyFrom":"AMS","cityTo":"Paris","flyTo":"CDG","price":89,"route":[{"cityTo":"Paris","local_departure":"2026-10-10T08:00:00"}]}]}
    flight=FlightSearch._parse_flight_data(result)
    assert flight.destination_airport_code=="CDG"
    assert flight.price==89
    assert flight.stop_overs==0

def test_parse_connecting_flight():
    result={"data":[{"cityFrom":"Amsterdam","flyFrom":"AMS","cityTo":"Tokyo","flyTo":"NRT","price":500,"route":[{"cityTo":"Doha","local_departure":"2026-11-10T08:00:00"},{"cityTo":"Tokyo","local_departure":"2026-11-10T16:00:00"}]}]}
    flight=FlightSearch._parse_flight_data(result)
    assert flight.stop_overs==1
    assert flight.via_cities==["Doha"]

def test_parse_empty_result():
    assert FlightSearch._parse_flight_data({"data":[]}) is None
