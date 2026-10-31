from datetime import date
from sqlite3 import Row

from app.database import get_connection
from app.schemas import ExpenseCreate


def _to_dict(row: Row) -> dict:
    return dict(row)


def create_expense(expense: ExpenseCreate) -> dict:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO expenses (amount, category, description, expense_date)
            VALUES (?, ?, ?, ?)
            """,
            (
                expense.amount,
                expense.category.strip(),
                expense.description.strip(),
                expense.expense_date.isoformat(),
            ),
        )
        row = connection.execute(
            "SELECT * FROM expenses WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return _to_dict(row)


def list_expenses(category: str | None = None) -> list[dict]:
    with get_connection() as connection:
        if category:
            rows = connection.execute(
                "SELECT * FROM expenses WHERE lower(category) = lower(?) "
                "ORDER BY expense_date DESC, id DESC",
                (category,),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC"
            ).fetchall()
        return [_to_dict(row) for row in rows]


def delete_expense(expense_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM expenses WHERE id = ?", (expense_id,)
        )
        return cursor.rowcount > 0


def get_summary(start_date: date | None = None, end_date: date | None = None) -> dict:
    conditions = []
    parameters = []

    if start_date:
        conditions.append("expense_date >= ?")
        parameters.append(start_date.isoformat())
    if end_date:
        conditions.append("expense_date <= ?")
        parameters.append(end_date.isoformat())

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    with get_connection() as connection:
        totals = connection.execute(
            f"""
            SELECT COALESCE(SUM(amount), 0) AS total_spent,
                   COUNT(*) AS expense_count
            FROM expenses {where_clause}
            """,
            parameters,
        ).fetchone()

        category_rows = connection.execute(
            f"""
            SELECT category, SUM(amount) AS total
            FROM expenses {where_clause}
            GROUP BY category
            ORDER BY total DESC
            """,
            parameters,
        ).fetchall()

    return {
        "total_spent": round(totals["total_spent"], 2),
        "expense_count": totals["expense_count"],
        "by_category": [
            {"category": row["category"], "total": round(row["total"], 2)}
            for row in category_rows
        ],
    }
