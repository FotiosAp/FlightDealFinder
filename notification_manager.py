import requests
import os
import smtplib
from dotenv import load_dotenv
load_dotenv()
class NotificationManager:
    """
        Handles the delivery of alerts to the user.
        Supports sending direct messages via Telegram and mass emails via SMTP.
    """
    def __init__(self):
        self.api_token=os.environ["NOTIFICATION_API_TOKEN"]
        self.bot_id=os.environ["BOT_ID"]
        self.email_usn=os.environ["EMAIL_USN"]
        self.email_pswd=os.environ["EMAIL_PSW"]
    #This class is responsible for sending notifications with the deal flight details.
    def send_notification(self,price,departure_airport,destination_airport,out_date,return_date):
        """
            Sends a Telegram message with the flight deal details to a specific chat/bot ID.
        """
        URL= f"https://api.telegram.org/bot{self.api_token}/sendMessage"
        message = f"""Low Price Alert!
Only £{price} to fly from {departure_airport} to {destination_airport}.
📅 Dates: {out_date} until {return_date}."""
        data = {
            "chat_id":self.bot_id,
            "text":message
        }
        response=requests.post(url=URL,json=data)
        if response.status_code == 200:
            print("Success")
        else:
            print(response.text)
    def send_email(self,price,departure_airport,destination_airport,out_date,return_date,emails):
        """
            Loops through a list of customer emails and sends them an alert via Gmail SMTP.
        """
        with smtplib.SMTP("smtp.gmail.com",587) as smtp:
            smtp.starttls()
            smtp.login(self.email_usn,self.email_pswd)
            for email in emails:
                smtp.sendmail(from_addr=self.email_usn,
                              to_addrs=email,
                              msg=f"Subject:Low Price Alert!\n\nOnly ${price} to fly from {departure_airport} to {destination_airport}\n.📅 Dates: {out_date} until {return_date}.".encode('utf-8'))