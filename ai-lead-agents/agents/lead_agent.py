from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from tools.email_extractor import extract_emails
from tools.phone_extractor import extract_phone_numbers
from agents.agents import WebSearchTool

class LeadAgent:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        
        # Initialize WebSearchTool
        self.web_search_tool = WebSearchTool()

    def scrape_contact_info(self, url: str) -> dict:
        page = self.browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9",
        })
        stealth_sync(page)  # <-- Apply stealth here!
        page.goto(url)
        page.mouse.move(100, 100)
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        page.wait_for_timeout(2000)
        page_content = page.content()
        page.close()
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