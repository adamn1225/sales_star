import json
import os

# filepath: /home/adam/lead_scrape/ai-lead-agents/config.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")

# Load API keys from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

# Global API keys
OPENAI_API_KEY = config["api_keys"]["OPENAI_API_KEY"]
G_SHEETS_API = config["api_keys"]["G_SHEETS_API"]

# Example: Add other global settings if needed
SPREADSHEET_ID = "1Lhx66ttuPktLue_xKMOQmcTXjOxpibW54P7PssQiyD4"
CREDENTIALS_FILE = "credentials.json"