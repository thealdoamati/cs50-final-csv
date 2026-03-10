# CSV Importer (AI Facilitator)
#### Video Demo: https://youtu.be/Vayc528soX8
#### Description:

CSV Importer (AI Facilitator) is a Flask-based web application that helps you transform CSV files into structured outputs (TXT, JSON, CSV, grouped files, summaries, etc.) using Large Language Models — without consuming API tokens programmatically.

Instead of sending data via an API, the app generates a structured prompt from your CSV file and the requested action. You copy that prompt into any LLM (ChatGPT, Claude, Gemini, local models, etc.), receive a Python script in return, paste it into the provided template, and run it locally.

The system acts as a bridge between raw CSV data and AI-generated data processing scripts.

---

## How It Works

1. Run the Flask application.
2. Open the browser interface.
3. Upload a CSV file.
4. Describe the action you want to perform.

Example actions:
- Create a text file for each category, where each file contains rows with the same category.
- Generate a JSON file grouped by user ID.
- Create separate files per movie title.
- Export a summary CSV with totals per month.
- Remove duplicates and generate a cleaned dataset.

After confirmation, the application generates and downloads a ZIP package containing:


project_package.zip
├── input_csv/
│ └── csv_file.csv
├── output_files/
├── prompt.txt
└── script.py


- `input_csv/` contains your uploaded file.
- `prompt.txt` contains the generated instructions for the LLM.
- `script.py` is a placeholder where you paste the generated Python script.
- `output_files/` is where the script will write results.

You paste the prompt into an LLM, copy the generated script into `script.py`, and run it locally. If changes are needed, you can edit the action and regenerate the package.

---

## Key Design Choices

- No direct API integration. This avoids token costs, rate limits, and vendor lock-in.
- Sensitive fields (e.g., passwords, tokens, financial data) are masked in prompt examples.
- The app generates transformation logic, but execution happens locally.
- The structure enforces consistent folder organization (`input_csv`, `output_files`).

---

## Main Files

- `app.py` – Flask application handling upload, session management, prompt generation, and ZIP packaging.
- `helpers.py` – CSV validation and mock example generation with sensitive data masking.
- `prompts/base_prompt.txt` – Template used to generate the final LLM prompt.

---

## Running the Project

Install dependencies:


pip install flask pandas python-dotenv


Create a `.env` file:


SECRET_KEY=your_secret_key


Run the application:


python app.py


Open:


http://127.0.0.1:5000


CSV Importer (AI Facilitator) focuses on a single goal: converting CSV files into AI-generated, reusable data transformation scripts in a controlled, cost-efficient manner.
