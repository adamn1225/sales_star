from playwright.sync_api import sync_playwright
from tools.email_extractor import extract_emails
from tools.phone_extractor import extract_phone_numbers
from agents.agents import WebSearchTool

class LeadAgent:
    def __init__(self):
        # Initialize Playwright
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        # Initialize WebSearchTool
        self.web_search_tool = WebSearchTool()

    def scrape_contact_info(self, url: str) -> dict:
        """
        Scrape the given URL for emails and phone numbers using Playwright.
        """
        page = self.browser.new_page()
        page.goto(url)
        page_content = page.content()
        page.close()

        # Extract emails and phone numbers from the page content
        emails = extract_emails(page_content)
        phones = extract_phone_numbers(page_content)
        return {"emails": emails, "phones": phones}

    def perform_web_search(self, query: str) -> str:
        """
        Perform a web search using the WebSearchTool.
        """
        return self.web_search_tool.search(query)

    def close(self):
        """
        Close the Playwright browser and stop the Playwright instance.
        """
        try:
            self.browser.close()
        finally:
            self.playwright.stop()