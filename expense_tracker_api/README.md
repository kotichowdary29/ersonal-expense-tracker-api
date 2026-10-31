# Personal Expense Tracker API

A beginner-friendly Python API that helps a user record expenses, filter them by category,
delete incorrect entries, and view spending summaries.

## Features

- Create an expense with amount, category, description, and date
- List all expenses or filter by category
- Delete an expense
- View total spending and category totals
- Filter summaries by date range
- Validate input and return useful HTTP errors

## Tech stack

Python, FastAPI, SQLite, Pydantic, pytest.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the interactive API documentation.

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/expenses` | Create an expense |
| GET | `/expenses` | List expenses |
| GET | `/expenses?category=Food` | Filter by category |
| DELETE | `/expenses/{expense_id}` | Delete an expense |
| GET | `/summary` | Total and category breakdown |
| GET | `/summary?start_date=2026-10-01&end_date=2026-10-31` | Date-filtered summary |

## Example request

```json
{
  "amount": 125.5,
  "category": "Food",
  "description": "Lunch",
  "expense_date": "2026-10-31"
}
```

## Run tests

```bash
pytest
```

## Design

- `main.py`: HTTP routes and request-level validation
- `schemas.py`: request and response models
- `repository.py`: SQL queries and database operations
- `database.py`: SQLite connection and schema initialization
- `tests/`: API tests

SQL queries use parameterized values to avoid SQL injection. The project intentionally
uses SQLite's standard library rather than adding an ORM, keeping the database layer
easy to inspect and understand.
