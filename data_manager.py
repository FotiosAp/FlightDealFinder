from dotenv import load_dotenv
load_dotenv()
import requests
import os
class DataManager:
    """
        This class is responsible for communicating with the Google Sheet via the Sheety API.
        It fetches destinations, updates lowest prices, and retrieves user emails.
    """
    def __init__(self):
        self.destination_data={}
        self.api_prices=os.environ.get("API_SHEET_ENDPOINT_PRICES")
        self.api_users=os.environ.get("API_SHEET_ENDPOINT_USERS")
        self.username=os.environ.get("SHEETY_USERNAME")
        self.password=os.environ.get("SHEETY_PASSWORD")
    #This class is responsible for talking to the Google Sheet.
    def get_destination_data(self):
        """
            Fetches the list of destinations and their target prices from the Google Sheet.
        """
        response = requests.get(url=self.api_prices,auth=(self.username,self.password))
        data= response.json()
        self.destination_data=data["prices"]
        return self.destination_data
    def update_lowest_price(self,new_lowest_price,row):
        """
            Updates the Google Sheet with the newly found lowest price for a specific destination.
        """
        cheapest_flight_data={
            "price":{
                "lowestPrice":new_lowest_price
            }
        }
        put_url=f"{self.api_prices}/{row}"
        response_update_sheet = requests.put(url=put_url,json=cheapest_flight_data,auth=(self.username,self.password))
    def get_customer_emails(self):
        """
            Retrieves all registered customer emails from the users tab in the Google Sheet.
        """
        response_emails = requests.get(url=self.api_users,auth=(self.username,self.password))
        data_emails=response_emails.json()
        return data_emails["users"]
