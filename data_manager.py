from dotenv import load_dotenv
load_dotenv()
import requests
import os
class DataManager:
    def __init__(self):
        self.destination_data={}
        self.api_prices=os.environ.get("API_SHEET_ENDPOINT_PRICES")
        self.api_users=os.environ.get("API_SHEET_ENDPOINT_USERS")
        self.username=os.environ.get("SHEETY_USERNAME")
        self.password=os.environ.get("SHEETY_PASSWORD")
    #This class is responsible for talking to the Google Sheet.
    def get_destination_data(self):
        response = requests.get(url=self.api_prices,auth=(self.username,self.password))
        data= response.json()
        self.destination_data=data["prices"]
        return self.destination_data
    def update_lowest_price(self,new_lowest_price,row):
        cheapest_flight_data={
            "price":{
                "lowestPrice":new_lowest_price
            }
        }
        put_url=f"{self.api_prices}/{row}"
        response_update_sheet = requests.put(url=put_url,json=cheapest_flight_data,auth=(self.username,self.password))
    def get_customer_emails(self):
        response_emails = requests.get(url=self.api_users,auth=(self.username,self.password))
        data_emails=response_emails.json()
        return data_emails["users"]
