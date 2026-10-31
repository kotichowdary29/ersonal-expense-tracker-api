from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(default="", max_length=200)
    expense_date: date


class ExpenseResponse(ExpenseCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CategoryTotal(BaseModel):
    category: str
    total: float


class ExpenseSummary(BaseModel):
    total_spent: float
    expense_count: int
    by_category: list[CategoryTotal]
