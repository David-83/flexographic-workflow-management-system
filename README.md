# Flexographic Workflow Management System

MSIT 5910 capstone repository for a centralized plate-request, workflow, inventory, alert, and reporting prototype.

## Structure
- `src/` application source
- `docs/` requirements and technical documentation
- `design/` architecture and design artifacts
- `tests/` test cases

## Branching
- `main`: reviewed milestone work
- `development`: active integration work
  
## Development Progress

Initial system architecture, requirements, and project structure have been prepared for the MSIT 5910 capstone project.

## Functional Flask Prototype – Final Capstone Update

The Flexographic Plate Workflow Management System is an academic software prototype developed for MSIT 5910 at the University of the People.

The project addresses fragmented production information and communication between schedulers, plate makers, plate mounters, and other manufacturing stakeholders.

### Implemented Features

- Web-based dashboard displaying plate requests and current workflow statuses.
- New plate-request form with job number, job name, department, quantity, and priority.
- Workflow-status updates, including Requested and Plate Making.
- SQLite database for storing and retrieving request information.
- Server-side validation for required fields, positive integer quantities, and supported workflow statuses.
- Inventory information interface.
- Parameterized SQL statements for database operations.

### Technology Stack

- Python – application programming
- Flask – web application framework
- SQLite – relational database
- HTML and CSS – frontend interface
- pytest and pytest-cov – automated testing

### Project Organization

The working application is located in the `flask-app/` directory.

The original `src/`, `tests/`, `design/`, and `docs/` directories preserve the earlier project development materials and documentation.

### Running the Prototype

The application can be run locally on Windows, macOS, or Linux.

From the `flask-app` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

On Windows, activate the virtual environment using the appropriate `venv\Scripts` command.

Open the application at http://127.0.0.1:5000.

### Testing and Evaluation

The latest verified Windows application completed all 10 automated pytest tests successfully, with 79% statement coverage.

Testing covered page availability, request creation, database persistence, input validation, and workflow-status updates.

Local performance testing previously recorded a median dashboard response time of 11.60 milliseconds across 30 measured requests.

These results describe prototype testing, not full production readiness.

### Future Enhancements

Planned improvements include authentication, role-based permissions, advanced inventory tracking, automated alerts, audit logs, backup and recovery testing, concurrent-user support, and possible integration with SAP and other approved manufacturing systems.

### Project Status

Functional academic prototype. Further security, reliability, and deployment testing is required before use in a production manufacturing environment.
