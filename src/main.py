import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Employee Data Service")

DATA_FILE = Path(__file__).resolve().parent.parent / "employees.json"


class Employee(BaseModel):
    name: str = Field(min_length=1)
    department: str = "General"
    salary: float = Field(gt=0)


def read_employees() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_employees(employees: list[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/employees")
def get_employees():
    return read_employees()


@app.get("/employees/{name}")
def get_employee(name: str):
    employees = read_employees()

    for employee in employees:
        if employee.get("name", "").lower() == name.lower():
            return employee

    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: Employee):
    employees = read_employees()
    new_employee = employee.model_dump()
    employees.append(new_employee)
    save_employees(employees)
    return new_employee
