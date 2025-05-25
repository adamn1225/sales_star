# AI Lead Agents

This project implements AI agents for gathering and organizing leads. The main components of the project include a `LeadAgent` for scraping leads and a `LeadOrganizer` for categorizing and storing them in Google Sheets.

## Project Structure

```
ai-lead-agents
├── src
│   ├── agents
│   │   ├── lead_agent.py        # Defines the LeadAgent class for gathering leads
│   │   ├── lead_organizer.py     # Defines the LeadOrganizer class for organizing leads
│   │   └── __init__.py           # Initializes the agents module
│   ├── tools
│   │   ├── web_search.py         # Contains a function for web searching leads
│   │   ├── email_extractor.py     # Contains a function for extracting emails
│   │   ├── phone_extractor.py      # Contains a function for extracting phone numbers
│   │   └── __init__.py           # Initializes the tools module
│   ├── services
│   │   ├── google_sheets_service.py # Defines the GoogleSheetsService class for interacting with Google Sheets
│   │   └── __init__.py           # Initializes the services module
│   ├── main.py                    # Entry point for the application
│   └── types
│       └── __init__.py           # Initializes the types module
├── requirements.txt               # Lists project dependencies
├── .env                           # Contains environment variables
├── README.md                      # Project documentation
└── .gitignore                     # Specifies files to ignore in version control
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-lead-agents
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in the `.env` file, including API keys and credentials for Google Sheets.

## Usage

To start the lead gathering and organizing process, run the main application:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.