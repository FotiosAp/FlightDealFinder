class FlightData:
    """
        A structured class that holds the details of a single flight deal.
    """
    def __init__(self,price,origin_airport,destination_airport,out_date,return_date,nr_stops):
        self.price=price
        self.origin_airport=origin_airport
        self.destination_airport=destination_airport
        self.out_date=out_date
        self.return_date=return_date
        self.stops=nr_stops
def find_cheapest_flight(data,return_date):
    """
        Parses the raw JSON data returned by the Flight Search API.
        Finds and returns the cheapest flight object among all options.
    """
    if data is None:
        return FlightData(price="N/A", origin_airport="N/A", destination_airport="N/A", out_date="N/A",return_date="N/A",nr_stops="N/A")
    best_flights = data.get("best_flights", [])
    other_flights = data.get("other_flights", [])
    total_flights=best_flights+other_flights
    lowest_price=float("inf")
    cheapest_flight_data=None
    if not total_flights:
        print("No flights found.")
        return FlightData(price="N/A", origin_airport="N/A", destination_airport="N/A", out_date="N/A",return_date="N/A",nr_stops="N/A")
    for flight in total_flights:
        try:
            flight_price=flight["price"]
            if flight_price<=lowest_price:
                lowest_price=flight_price
                cheapest_flight_data=flight
        except KeyError:
            continue
    #Construct and return the FlightData object with the cheapest flight details
    return FlightData(price=lowest_price,
                      origin_airport=cheapest_flight_data["flights"][0]["departure_airport"]["id"],
                      destination_airport=cheapest_flight_data["flights"][-1]["arrival_airport"]["id"],
                      out_date=cheapest_flight_data["flights"][0]["departure_airport"]["time"].split(" ")[0],
                      return_date=return_date,
                      nr_stops=len(cheapest_flight_data["flights"])-1
                      )


