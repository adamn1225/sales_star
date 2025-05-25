import sqlite3
from services.google_sheets_service import GoogleSheetsService

class LeadOrganizer:
    def __init__(self, sheets_service: GoogleSheetsService, db_path="leads.db"):
        self.sheets_service = sheets_service
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                emails TEXT,
                phones TEXT,
                research TEXT,
                intent TEXT,
                prospect_analysis TEXT,
                outreach_template TEXT
            )
        """)
        conn.commit()
        conn.close()

    def store_lead(self, lead: dict):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO leads (company_name, emails, phones, research, intent, prospect_analysis, outreach_template)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lead.get("company_name", ""),
            ";".join(lead.get("emails", [])),  # Use semicolon
            ";".join(map(str, lead.get("phones", []))),  # Use semicolon
            lead.get("research", ""),
            lead.get("intent", ""),
            lead.get("prospect_analysis", ""),
            lead.get("outreach_template", "")
        ))
        conn.commit()
        conn.close()

    def get_leads(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT company_name, emails, phones, research, intent, prospect_analysis, outreach_template FROM leads")
        rows = c.fetchall()
        conn.close()
        leads = []
        for row in rows:
            leads.append({
                "company_name": row[0],
                "emails": row[1].split(";") if row[1] else [],
                "phones": row[2].split(";") if row[2] else [],
                "research": row[3],
                "intent": row[4],
                "prospect_analysis": row[5],
                "outreach_template": row[6],
            })
        return leads

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
    
    def delete_lead(self, company_name: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM leads WHERE company_name = ?", (company_name,))
        conn.commit()
        conn.close()