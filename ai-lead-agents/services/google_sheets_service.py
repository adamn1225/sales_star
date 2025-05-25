from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from typing import Any, List

class GoogleSheetsService:
    def __init__(self, spreadsheet_id: str, credentials_file: str):
        """
        Initialize the Google Sheets service.

        Args:
            spreadsheet_id (str): The ID of the Google Sheets document.
            credentials_file (str): Path to the service account credentials JSON file.
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials = Credentials.from_service_account_file(credentials_file)
        self.service = build('sheets', 'v4', credentials=self.credentials)

    def append_lead(self, lead_data: dict, category: str) -> None:
        range_name = f"'{category}'!A1"  # Enclose the category in single quotes
        values = [[
            lead_data.get("company_name", ""),
            ", ".join(map(str, lead_data.get("phones", []))),  # Convert phone numbers to strings
            ", ".join(lead_data.get("emails", [])),
            lead_data.get("research", ""),
            lead_data.get("intent", ""),
            lead_data.get("prospect_analysis", ""),
            lead_data.get("outreach_template", "")
        ]]
        body = {"values": values}

        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
        except Exception as e:
            print(f"Error appending lead to category '{category}': {e}")
            raise

    def create_category_tab(self, category: str) -> None:
        """
        Create a new tab (sheet) in the Google Sheets document for the specified category.

        Args:
            category (str): The name of the new tab to create.
        """
        requests = [{
            'addSheet': {
                'properties': {
                    'title': category
                }
            }
        }]
        body = {'requests': requests}

        try:
            self.service.spreadsheets().batchUpdate(  # type: ignore
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()  # type: ignore
        except Exception as e:
            print(f"Error creating category tab '{category}': {e}")
            raise
        
    def get_sheets(self) -> List[dict]:
        """
        Retrieve the titles and IDs of all sheets (tabs) in the Google Sheets document.

        Returns:
            List[dict]: A list of dictionaries containing 'title' and 'sheetId' for each tab.
        """
        try:
            response = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            sheets = response.get('sheets', [])
            return [{"title": sheet['properties']['title'], "sheetId": sheet['properties']['sheetId']} for sheet in sheets]
        except Exception as e:
            print(f"Error retrieving sheets: {e}")
            raise

    def append_lead_by_sheet_id(self, lead_data: dict, sheet_id: int) -> None:
        """
        Append a lead to the specified sheet using its sheetId.

        Args:
            lead_data (dict): The lead data containing 'name', 'email', and 'phone'.
            sheet_id (int): The ID of the sheet to append the lead to.
        """
        # Use the sheetId to construct the range
        range_name = f"'{sheet_id}'!A1"  # Use the sheetId in the range
        values = [[lead_data.get('name'), lead_data.get('email'), lead_data.get('phone')]]
        body = {'values': values}

        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
        except Exception as e:
            print(f"Error appending lead to sheet ID '{sheet_id}': {e}")
            raise