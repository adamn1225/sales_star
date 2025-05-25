import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QGroupBox, QSplitter, QHBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from agents.sales_agent import SalesAgent
from services.google_sheets_service import GoogleSheetsService
from agents.lead_organizer import LeadOrganizer
from config import OPENAI_API_KEY, G_SHEETS_API, SPREADSHEET_ID, CREDENTIALS_FILE
import markdown

class CRMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prospect Management CRM")
        self.setGeometry(200, 200, 1400, 900)
        self.setStyleSheet("background-color: #0f172a; font-family: Arial, sans-serif;color: #f0f2f7;")
        self.setWindowIconText("Prospect Management CRM")

        # Initialize Google Sheets service
        self.sheets_service = GoogleSheetsService(SPREADSHEET_ID, CREDENTIALS_FILE)
        self.sales_agent = SalesAgent(self.sheets_service)

        # Retrieve the sheetId for the "pyleads" tab
        sheets = self.sheets_service.get_sheets()
        sheet_id = None
        for sheet in sheets:
            if sheet["title"] == "pyleads":
                sheet_id = sheet["sheetId"]
                break
        if sheet_id:
            print(f"Sheet ID for 'pyleads': {sheet_id}")
        else:
            print("Tab 'pyleads' not found.")

        # Store detailed results for sidebar
        self.detailed_results = []

        # --- SIDEBAR (INFO TAB) ---
        self.info_tab = QGroupBox("Info Tab")
        self.info_tab.setMinimumWidth(400)

        # Create the text widgets once
        self.research_text = QTextEdit()
        self.research_text.setReadOnly(True)
        self.intent_text = QTextEdit()
        self.intent_text.setReadOnly(True)
        self.prospect_text = QTextEdit()
        self.prospect_text.setReadOnly(True)
        self.outreach_text = QTextEdit()
        self.outreach_text.setReadOnly(True)

        def make_section(title, widget):
            group = QGroupBox(title)
            group.setCheckable(True)
            group.setChecked(True)  # Default expanded
            layout = QVBoxLayout()
            layout.addWidget(widget)
            group.setLayout(layout)
            return group

        # Use a vertical splitter for resizable/collapsible sections
        self.sidebar_splitter = QSplitter(Qt.Orientation.Vertical)
        self.sidebar_splitter.addWidget(make_section("Research Agent", self.research_text))
        self.sidebar_splitter.addWidget(make_section("Intent Agent", self.intent_text))
        self.sidebar_splitter.addWidget(make_section("Prospect Agent", self.prospect_text))
        self.sidebar_splitter.addWidget(make_section("Outreach Agent", self.outreach_text))

        # Set the splitter as the only widget in the sidebar groupbox
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.sidebar_splitter)
        self.info_tab.setLayout(sidebar_layout)

        # --- LEFT SIDE (INPUTS + TABLE) ---
        self.layout = QVBoxLayout()
        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter the URL of the company website")
        self.url_input.setStyleSheet("""
            QLineEdit {
            background-color: #1e293b; 
            color: #fafafa; 
            padding: 10px; 
            border-radius: 5px;
            }
            QLineEdit:hover {
            background-color: #334155;
            }
        """)
        self.company_label = QLabel("Company Name:")
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("Enter the company name")
        self.company_input.setStyleSheet("""
            QLineEdit {
            background-color: #1e293b; 
            color: #f5f5f5; 
            padding: 10px; 
            border-radius: 5px;
            }
            QLineEdit:hover {
            background-color: #334155;
            }
        """)
        self.submit_button = QPushButton("Run Workflow")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #003eb3;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0646bf;
            }
            QToolTip {
                background-color: #3f4a5c;
                color: #f0f2f7;
                border: 1px solid #334155;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_button.setToolTip("Click to run the workflow")
        # Set custom tooltip style for the button only
        self.submit_button.clicked.connect(self.run_workflow)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Company Name", "Phone", "Email", "Delete"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.update_info_tab)
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.company_label)
        self.layout.addWidget(self.company_input)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.table)

        # --- SPLITTER ---
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(self.layout)
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(self.info_tab)
        self.splitter.setSizes([900, 500])

        # --- CENTRAL WIDGET ---
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addWidget(self.splitter)
        container.setLayout(container_layout)
        self.setCentralWidget(container)

        # --- Initialize LeadOrganizer and load leads from SQLite ---
        self.lead_organizer = LeadOrganizer(self.sheets_service)
        leads = self.lead_organizer.get_leads()
        for lead in leads:
            self.add_results_to_table(lead)

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

        self.add_results_to_table(results)
        
    def add_results_to_table(self, results: dict):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(results["company_name"]))
        self.table.setItem(row_position, 1, QTableWidgetItem(", ".join(map(str, results["phones"]))))
        self.table.setItem(row_position, 2, QTableWidgetItem(", ".join(results["emails"])))
        # Add Delete button with fixed width and centered
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedWidth(80)  # Set button width
        delete_btn.setStyleSheet("background-color: #b91c1c; color: white; border-radius: 4px; padding: 5px;")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda _, row=row_position: self.delete_row(row))
        # Center the button in the cell
        cell_widget = QWidget()
        layout = QHBoxLayout(cell_widget)
        layout.addWidget(delete_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        cell_widget.setLayout(layout)
        self.table.setCellWidget(row_position, 3, cell_widget)
        # Store the rest for the sidebar
        self.detailed_results.append({
            "research": results["research"],
            "intent": results["intent"],
            "prospect_analysis": results["prospect_analysis"],
            "outreach_template": results["outreach_template"]
        })

    def update_info_tab(self):
        selected = self.table.currentRow()
        if selected >= 0 and selected < len(self.detailed_results):
            details = self.detailed_results[selected]
            self.research_text.setHtml(markdown.markdown(details["research"]))
            self.intent_text.setHtml(markdown.markdown(details["intent"]))
            self.prospect_text.setHtml(markdown.markdown(details["prospect_analysis"]))
            self.outreach_text.setHtml(markdown.markdown(details["outreach_template"]))
        else:
            self.research_text.clear()
            self.intent_text.clear()
            self.prospect_text.clear()
            self.outreach_text.clear()

    def delete_row(self, row):
        company_name_item = self.table.item(row, 0)
        if not company_name_item:
            return
        company_name = company_name_item.text()
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{company_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.lead_organizer.delete_lead(company_name)
            self.table.removeRow(row)
            if row < len(self.detailed_results):
                del self.detailed_results[row]

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