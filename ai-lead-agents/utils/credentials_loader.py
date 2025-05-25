# filepath: /home/adam/lead_scrape/src/utils/credentials_loader.py
import json

def load_credentials(file_path: str):
    """
    Load credentials from a JSON file.

    Args:
        file_path (str): Path to the credentials JSON file.

    Returns:
        dict: A dictionary containing the credentials.
    """
    with open(file_path, "r") as file:
        return json.load(file)