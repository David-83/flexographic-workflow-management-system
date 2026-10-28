# Flexographic Plate Workflow Management System – Working Prototype

This directory contains the functional Flask and SQLite prototype developed for the MSIT 5910 capstone project.

## Main Features

- Create new flexographic plate requests.
- Display saved requests on a centralized dashboard.
- Update production workflow statuses.
- Store and retrieve request records using SQLite.
- Reject invalid quantities, missing required fields, and unsupported workflow statuses.
- Display the prototype's inventory interface.

## Technology Stack

Python, Flask, SQLite, HTML, CSS, and pytest.

## Testing

The latest verified Windows development environment passed all 10 automated tests with 79% statement coverage.

## Running the Application

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

The application is an academic prototype and is not intended for production deployment without additional security, concurrency, and backup-recovery testing.
