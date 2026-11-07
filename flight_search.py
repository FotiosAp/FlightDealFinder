import os
import requests
from dotenv import load_dotenv
load_dotenv()
class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_key = os.environ.get("SERP_API_KEY")
    def check_flights(self,origin_city_code,destination_city_code,from_time,to_time,is_direct):
        if is_direct:
            stops="1"
        else:
            stops="0"
        flights_info={
            "engine":"google_flights",
            "departure_id":origin_city_code,
            "arrival_id":destination_city_code,
            "outbound_date":from_time,
            "return_date":to_time,
            "type":"1",
            "adults":"1",
            "currency":"EUR",
            "stops":stops,
            "api_key":self.api_key
        }
        response_flight=requests.get(url="https://serpapi.com/search",params=flights_info)
        return response_flight.json()
        # print(response_flight.json())