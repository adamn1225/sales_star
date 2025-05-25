from agents.lead_agent import LeadAgent
from agents.lead_organizer import LeadOrganizer
from agents.research_agent import ResearchAgent
from agents.intent_agent import FindIntentAgent
from agents.prospect_agent import ProspectAgent
from agents.outreach_agent import OutreachAgent
from services.google_sheets_service import GoogleSheetsService
import json
import os
from datetime import datetime, timezone
from config import OPENAI_API_KEY, SPREADSHEET_ID, CREDENTIALS_FILE
import openai


class SalesAgent:
    def __init__(self, sheets_service: GoogleSheetsService):
        # Use global settings from config.py
        self.sheets_service = sheets_service
        self.lead_organizer = LeadOrganizer(sheets_service)

        # Set OpenAI API key globally

        # Initialize LeadAgent
        self.lead_agent = LeadAgent()

    def run_agent_chain(self, url: str, company: str, goal: str = "logistics", industry: str = "industrial equipment", sender_name: str = "Noah", sender_company: str = "Heavy Haulers") -> dict:
        try:
            # Step 1: Scrape Contact Info
            print(f"Scraping contact info for URL: {url}")
            contact_info = self.lead_agent.scrape_contact_info(url)
            print("=== Lead Agent Output ===")
            print(contact_info)
        except Exception as e:
            print(f"Error in LeadAgent: {e}")
            contact_info = {"emails": [], "phones": []}

        try:
            # Step 2: Store Initial Lead
            print("Storing initial lead data...")
            initial_lead_data = {
                "company_name": company,
                "emails": contact_info["emails"],
                "phones": contact_info["phones"],
            }
            self.lead_organizer.store_lead(initial_lead_data)
        except Exception as e:
            print(f"Error in LeadOrganizer: {e}")

        try:
            # Step 3: Research Agent
            research_agent = ResearchAgent()
            research = research_agent.run(company, goal)
            print("=== Research Agent Output ===")
            print(research)
        except Exception as e:
            print(f"Error in ResearchAgent: {e}")
            research = "No research data available."

        try:
            # Step 4: Find Intent Agent
            intent_agent = FindIntentAgent()
            intent = intent_agent.run(company, industry)
            print("=== Find Intent Agent Output ===")
            print(intent)
        except Exception as e:
            print(f"Error in FindIntentAgent: {e}")
            intent = "N/A"

        try:
            # Step 5: Prospect Agent
            prospect_agent = ProspectAgent()
            prospect = prospect_agent.run(company, research, intent)
            print("=== Prospect Agent Output ===")
            print(prospect)
        except Exception as e:
            print(f"Error in ProspectAgent: {e}")
            prospect = "N/A"

        try:
            # Step 6: Outreach Agent
            outreach_agent = OutreachAgent()
            outreach = outreach_agent.run(company, research, intent, prospect)
            print("=== Outreach Agent Output ===")
            print(outreach)
        except Exception as e:
            print(f"Error in OutreachAgent: {e}")
            outreach = "N/A"

        # Step 7: Save Final Results
        result_data = {
            "company_name": company,
            "emails": contact_info["emails"],
            "phones": contact_info["phones"],
            "goal": goal,
            "industry": industry,
            "research": research,
            "intent": intent,
            "prospect_analysis": prospect,
            "outreach_template": outreach,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        try:
            print("Saving results to Google Sheets...")
            self.sheets_service.append_lead(result_data, "pyleads")
        except Exception as e:
            print(f"Error saving to Google Sheets: {e}")

        try:
            print("Saving results to local file...")
            os.makedirs("output", exist_ok=True)
            filename = f"output/{company.replace(' ', '_').replace('/', '_').replace(':', '_')}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(result_data, f, indent=2)
            print(f"\n📁 Results saved to: {filename}")
        except Exception as e:
            print(f"Error saving to local file: {e}")

        return result_data

    def close(self):
        """
        Close any resources used by the SalesAgent.
        """
        self.lead_agent.close()