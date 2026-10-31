from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, HTTPException, Query, status

from app.database import initialize_database
from app import repository
from app.schemas import ExpenseCreate, ExpenseResponse, ExpenseSummary


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Personal Expense Tracker API",
    description="A small API for recording expenses and understanding spending.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate):
    return repository.create_expense(expense)


@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(category: str | None = Query(default=None, min_length=1)):
    return repository.list_expenses(category)


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_expense(expense_id: int):
    if not repository.delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")


@app.get("/summary", response_model=ExpenseSummary)
def expense_summary(
    start_date: date | None = None,
    end_date: date | None = None,
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be on or before end_date",
        )
    return repository.get_summary(start_date, end_date)
