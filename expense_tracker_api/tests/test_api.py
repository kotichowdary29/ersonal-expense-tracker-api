from fastapi.testclient import TestClient

from app.main import app
from app import database


def test_expense_crud_and_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "test.db")

    with TestClient(app) as client:
        created = client.post(
            "/expenses",
            json={
                "amount": 125.50,
                "category": "Food",
                "description": "Lunch",
                "expense_date": "2026-10-31",
            },
        )
        assert created.status_code == 201
        expense_id = created.json()["id"]

        listed = client.get("/expenses?category=food")
        assert listed.status_code == 200
        assert len(listed.json()) == 1

        summary = client.get("/summary")
        assert summary.json()["total_spent"] == 125.5
        assert summary.json()["expense_count"] == 1

        deleted = client.delete(f"/expenses/{expense_id}")
        assert deleted.status_code == 204
        assert client.delete(f"/expenses/{expense_id}").status_code == 404


def test_rejects_non_positive_amount(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "test.db")

    with TestClient(app) as client:
        response = client.post(
            "/expenses",
            json={
                "amount": 0,
                "category": "Food",
                "description": "",
                "expense_date": "2026-10-31",
            },
        )
        assert response.status_code == 422
