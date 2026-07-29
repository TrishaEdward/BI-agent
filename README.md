BI Agent
Bi Agent is a business intelligence dashboard and assistant built with Streamlit. It connects to monday.com boards to fetch deal and work order data, normalizes the data for analysis, generates AI-powered insights, and produces report documents.

## Features

- Connects to monday.com using the monday.com GraphQL API
- Loads, sanitizes, and converts deal/work order data into pandas DataFrames
- Provides AI-driven business insights using Groq’s chat API
- Builds interactive Streamlit visualizations
- Generates BI report documents from a Word template
- Supports a chat-style question flow for business analysis

## Requirements

- Python 3.10+ (recommended)
- `pip install -r requirements.txt`

Required packages are listed in `requirements.txt`:

- streamlit
- pandas
- plotly
- requests
- python-dotenv
- groq
- python-docx

## Setup

1. Clone or copy the repository.
2. Create a `.env` file in the project root.
3. Add the required environment variables:

```env
MONDAY_API_KEY=your_monday_api_key
DEALS_BOARD_ID=your_deals_board_id
WORK_BOARD_ID=your_work_orders_board_id
GROQ_API_KEY=your_groq_api_key
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

Open the URL that Streamlit prints in your terminal.

## Project Structure

- `app.py` - Streamlit dashboard and UI logic
- `monday_client.py` - monday.com API client and board data fetches
- `data_processor.py` - data loading and normalization for deals and work orders
- `query_agent.py` - business question intent detection, KPI computation, and AI prompt orchestration
- `insights_engine.py` - chart creation and metrics extraction
- `report_generator.py` - Word report generation using a `.docx` template
- `BI report.docx` - report template file used by `report_generator.py`

## How It Works

1. `monday_client.py` queries monday.com boards and returns row data.
2. `data_processor.py` converts the raw data into pandas DataFrames, converting numeric and date fields where available.
3. `query_agent.py` analyzes the user’s question, calculates key business metrics, and calls the Groq API to generate a narrative answer.
4. `insights_engine.py` creates visual chart objects from the processed DataFrames.
5. `report_generator.py` generates a `.docx` report based on user-selected sections and AI insights.

## Environment Variables

- `MONDAY_API_KEY` - monday.com API key for GraphQL access
- `DEALS_BOARD_ID` - monday.com board ID for deal records
- `WORK_BOARD_ID` - monday.com board ID for work order records
- `GROQ_API_KEY` - Groq API key for LLM / chat completions

## Notes

- Ensure `BI report.docx` exists in the repository root if you want to generate reports.
- The dashboard uses Streamlit session state to manage chat history and selected visualizations.
- Column discovery in data processing is flexible, but board column titles should include keywords like `value`, `sector`, `stage`, or `probability`.

## Troubleshooting

- If data fails to load, verify your monday.com API key and board IDs.
- If the AI analysis fails, verify `GROQ_API_KEY` is set and valid.
- For date or numeric conversion issues, inspect the monday.com column value formats.

## License

This repository does not include a license file. Add one if you plan to share the project publicly.
