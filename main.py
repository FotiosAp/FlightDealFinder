#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests_cache
from data_manager import DataManager
from pprint import pprint
from datetime import datetime,timedelta
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager
#Set up the search window (tomorrow to 6 months from today)
today=datetime.today().date()
tomorrow =today + timedelta(days=1)
six_months_from_today=today+timedelta(days=180)
#Configure caching to save API calls (1 hour for SerpAPI, 0 for Sheety to always get fresh data)
cache_filters={
    "*api.sheety.co*":0,# Πιάνει αυτόματα το δικό σου endpoint γιατί περιέχει αυτό το κομμάτι
    "*":3600# Οτιδήποτε άλλο (δηλαδή το SerpAPI), κράτα το για 1 ώρα
}
requests_cache.install_cache(cache_name="flight_cache_data",backend='sqlite',urls_expire_after=cache_filters)
data = DataManager()#create the object
sheet_data=data.get_destination_data()#klhsh ths methodoy kai me to return bazv to sheet sthn var sheet data
customer_data = data.get_customer_emails()
#Extract all customer emails into a simple list
email_list=[]
for customer in customer_data:
    email_list.append(customer["whatIsYourEmail?"])
# pprint(email_list)
# print(sheet_data)
# pprint(sheet_data)
# return_test_data=tomorrow+timedelta(days=4)
flight_search=FlightSearch()
notification=NotificationManager()
#Loop through all destinations in the Google Sheet to find flight deals
for destination in sheet_data:
    flight_data=flight_search.check_flights(
        origin_city_code="LHR",
        destination_city_code=destination["iataCode"],
        from_time=tomorrow.strftime("%Y-%m-%d"),
        to_time=six_months_from_today.strftime("%Y-%m-%d"),
        is_direct=True
    )
    cheapest_flight = find_cheapest_flight(flight_data, six_months_from_today.strftime("%Y-%m-%d"))
    if cheapest_flight.price != "N/A":
        if cheapest_flight.price <=destination["lowestPrice"]:
            # print(f"Found a cheapest flight for {destination["city"]} with price of {cheapest_flight.price}")
            print(f"Direct flight to {destination['city']}.")
            notification.send_notification(cheapest_flight.price,cheapest_flight.origin_airport,cheapest_flight.destination_airport,cheapest_flight.out_date,cheapest_flight.return_date)
            notification.send_email(cheapest_flight.price,cheapest_flight.origin_airport,cheapest_flight.destination_airport,cheapest_flight.out_date,cheapest_flight.return_date,email_list)
            data.update_lowest_price(cheapest_flight.price, destination["id"])
        else:
            print(f"The flight for {destination["city"]} costs {cheapest_flight.price} which is not cheaper than the lowest price you had set")
    else:
        print(f"No direct flight to {destination['city']}. Looking for indirect flights...")
        #Fallback logic: Search for indirect flights if direct flights are unavailable
        flight_data = flight_search.check_flights(
            origin_city_code="LHR",
            destination_city_code=destination["iataCode"],
            from_time=tomorrow.strftime("%Y-%m-%d"),
            to_time=six_months_from_today.strftime("%Y-%m-%d"),
            is_direct=False
        )
        cheapest_flight = find_cheapest_flight(flight_data, six_months_from_today.strftime("%Y-%m-%d"))
        if cheapest_flight.price != "N/A":
            if cheapest_flight.price <= destination["lowestPrice"]:
                print(f"Found a cheapest flight for {destination['city']} with price of {cheapest_flight.price} but with {cheapest_flight.stops} stops.")
                notification.send_notification(cheapest_flight.price, cheapest_flight.origin_airport,
                                               cheapest_flight.destination_airport, cheapest_flight.out_date,
                                               cheapest_flight.return_date)
                notification.send_email(cheapest_flight.price, cheapest_flight.origin_airport,
                                        cheapest_flight.destination_airport, cheapest_flight.out_date,
                                        cheapest_flight.return_date,email_list)
                data.update_lowest_price(cheapest_flight.price, destination["id"])
            else:
                print(f"The flight for {destination["city"]} costs {cheapest_flight.price} which is not cheaper than the lowest price you had set")

