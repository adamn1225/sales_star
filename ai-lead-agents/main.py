import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from agents.sales_agent import SalesAgent
from services.google_sheets_service import GoogleSheetsService
from config import OPENAI_API_KEY, G_SHEETS_API, SPREADSHEET_ID, CREDENTIALS_FILE


class CRMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lead Management CRM")
        self.setGeometry(100, 100, 800, 600)

        # Initialize Google Sheets service
        self.sheets_service = GoogleSheetsService(SPREADSHEET_ID, CREDENTIALS_FILE)

        # Initialize SalesAgent
        self.sales_agent = SalesAgent(self.sheets_service)

        # Retrieve the sheetId for the "pyleads" tab
        sheets = self.sheets_service.get_sheets()
        sheet_id = None
        for sheet in sheets:
            if sheet["title"] == "pyleads":  # Replace "pyleads" with your tab name
                sheet_id = sheet["sheetId"]
                break

        if sheet_id:
            print(f"Sheet ID for 'pyleads': {sheet_id}")
        else:
            print("Tab 'pyleads' not found.")

        # Main layout
        self.layout = QVBoxLayout()

        # Input fields
        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.company_label = QLabel("Company Name:")
        self.company_input = QLineEdit()

        # Submit button
        self.submit_button = QPushButton("Run Workflow")
        self.submit_button.clicked.connect(self.run_workflow)

        # Table for CRM
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Company Name", "Phone", "Email", "Research", "Intent", "Prospect Analysis", "Outreach Template"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Add widgets to layout
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.company_label)
        self.layout.addWidget(self.company_input)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.table)

        # Set central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def run_workflow(self):
        # Get input values
        url = self.url_input.text()
        company = self.company_input.text()

        if not url or not company:
            self.statusBar().showMessage("Please enter both URL and Company Name.")
            return

        # Run the SalesAgent workflow
        try:
            results = self.sales_agent.run_agent_chain(
                url=url,
                company=company,
                goal="logistics",
                industry="industrial equipment",
                sender_name="Noah",
                sender_company="Heavy Haulers"
            )
            self.statusBar().showMessage("Workflow completed successfully!")
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}")
            return

        # Add results to the table
        self.add_results_to_table(results)

    def add_results_to_table(self, results: dict):
        # Add a new row to the table
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(results["company_name"]))
            self.table.setItem(row_position, 1, QTableWidgetItem(", ".join(map(str, results["phones"]))))  # Convert items to strings
            self.table.setItem(row_position, 2, QTableWidgetItem(", ".join(results["emails"])))
            self.table.setItem(row_position, 3, QTableWidgetItem(results["research"]))
            self.table.setItem(row_position, 4, QTableWidgetItem(results["intent"]))
            self.table.setItem(row_position, 5, QTableWidgetItem(results["prospect_analysis"]))
            self.table.setItem(row_position, 6, QTableWidgetItem(results["outreach_template"]))

    def closeEvent(self, event):
            # Ensure resources are cleaned up
            self.sales_agent.close()
            event.accept()

def main():
    app = QApplication(sys.argv)
    crm_app = CRMApp()
    crm_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()