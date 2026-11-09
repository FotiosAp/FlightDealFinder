# Flight Deal Finder ✈️

An automated, Object-Oriented Python application that continuously searches for the cheapest flight deals and alerts users when a flight's price drops below a specific target. 

## Key Features

- **Object-Oriented Architecture:** Clean, modular code split across dedicated classes (`DataManager`, `FlightSearch`, `FlightData`, `NotificationManager`).
- **Multi-API Integration:** Seamlessly connects with SerpAPI (Google Flights data), the Sheety API (Google Sheets integration), the Telegram Bot API, and Gmail SMTP.
- **Smart Caching Mechanism:** Utilizes `requests_cache` with a local SQLite backend to minimize redundant API calls and stay within free-tier rate limits.
- **Advanced Flight Logic:** Automatically checks for direct flights first, with a smart fallback to indirect flights (with stops) if direct routes are unavailable or too expensive.
- **Multi-Channel Alerts:** Dispatches instant low-price alerts via Telegram and sends mass HTML-formatted emails to a list of subscribed users.
- **Secure Credentials:** Keeps all API keys, passwords, and tokens safe using a `.env` environment variables setup.

## System Requirements

- Python 3.x
- `requests` and `requests_cache` libraries
- `python-dotenv` library
- A Google Sheet (connected via Sheety) with `prices` and `users` tabs.

## Setup & Installation

1. Clone the repository and ensure all `.py` files are in the same directory.
2. Create a file named `.env` in the root directory.
3. Add your API keys and credentials inside the `.env` file using the following format:

   ```env
   API_SHEET_ENDPOINT_PRICES=your_sheety_prices_endpoint
   API_SHEET_ENDPOINT_USERS=your_sheety_users_endpoint
   SHEETY_USERNAME=your_sheety_username
   SHEETY_PASSWORD=your_sheety_password
   SERP_API_KEY=your_serpapi_key
   NOTIFICATION_API_TOKEN=your_telegram_bot_token
   BOT_ID=your_telegram_chat_id
   EMAIL_USN=your_gmail_address
   EMAIL_PSW=your_gmail_app_password
