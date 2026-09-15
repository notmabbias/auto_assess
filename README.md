# Auto Assess v1.0

A lightweight, Flask-based diagnostic tool that cross-references vehicle specifications with established maintenance schedules and known issues to provide automated risk assessments.

## Features
* **Database Retrieval:** Queries local SQLite records for vehicle metadata, maintenance intervals, and critical failure points.
* **AI Analysis:** Integrates seller listing text and CARFAX data for LLM-driven risk evaluation.
* **Minimalist UI:** Vanilla HTML/JS frontend utilizing a lightweight, early-2000s brutalist aesthetic.

## Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML, Vanilla JavaScript

## Local Setup

1. Clone the repository:
```bash
git clone [https://github.com/notmabbias/auto-assess.git](https://github.com/notmabbias/auto-assess.git)
cd auto-assess
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

5. Initialize the database:
```bash
python3 database/create_db.py
```

6. Run the application:
```bash
flask run
```

The server will initialize at `http://127.0.0.1:5000`.
