from services.google_sheets_service import GoogleSheetsService

class LeadOrganizer:
    def __init__(self, sheets_service: GoogleSheetsService):
        self.sheets_service = sheets_service

    def categorize_lead(self, lead: dict) -> str:
        """
        Use OpenAI to categorize the lead.

        Args:
            lead (dict): The lead data.

        Returns:
            str: The category of the lead.
        """
        # Import Agent and Runner here to avoid circular import
        from agents import Agent, Runner

        prompt = f"Categorize the following lead into a category:\n{lead}"
        response = Runner.run_sync(
            Agent(
                name="Lead Categorizer",
                instructions="Categorize the lead into a specific category."
            ),
            prompt
        )
        return response.final_output.strip()