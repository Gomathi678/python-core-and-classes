import json

from fastapi.testclient import TestClient

import src.main as main
from src.main import DATA_FILE

client = TestClient(main.app)


def setup_function():
    DATA_FILE.write_text(
        json.dumps(
            [
                {"name": "Ravi", "department": "IT", "salary": 30000},
                {"name": "Priya", "department": "HR", "salary": 45000},
            ]
        ),
        encoding="utf-8",
    )


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_employee_success():
    response = client.get("/employees/Ravi")
    assert response.status_code == 200
    assert response.json()["name"] == "Ravi"


def test_get_employee_not_found():
    response = client.get("/employees/Unknown")
    assert response.status_code == 404


def test_invalid_salary():
    response = client.post(
        "/employees",
        json={"name": "Arun", "department": "Sales", "salary": -5},
    )
    assert response.status_code == 422


def test_empty_name():
    response = client.post(
        "/employees",
        json={"name": "", "department": "Sales", "salary": 25000},
    )
    assert response.status_code == 422


def test_missing_employee_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"
    monkeypatch.setattr(main, "DATA_FILE", missing_file)

    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json() == []
