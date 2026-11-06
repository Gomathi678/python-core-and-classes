import csv
import json
import logging
from pathlib import Path
from typing import List, Optional, Union

import fitz
from openpyxl import Workbook, load_workbook

# Configure logging
logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent


# 1. Convert salary into integer
def get_salary_value(salary: Union[int, str]) -> int:
    return int(salary)


# 2. Read employees from CSV
def read_employees() -> List[dict]:
    csv_path = BASE_DIR / "employees.csv"

    with open(csv_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        employees = list(reader)

    return employees


# 3. Write employees.json
def write_json(employees: List[dict]) -> None:
    json_path = BASE_DIR / "employees.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=4)

    print("employees.json created")


# 4. Write high earners CSV
def write_high_earners(employees: List[dict]) -> int:
    high_earners = [
        employee
        for employee in employees
        if get_salary_value(employee["salary"]) > 50000
    ]

    csv_path = BASE_DIR / "high_earners.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "department", "salary"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(high_earners)

    return len(high_earners)


# 5. Create and read Excel file
def create_salary_excel(employees: List[dict]) -> int:
    excel_path = BASE_DIR / "salary.xlsx"

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Employee Salaries"

    sheet.append(["Name", "Department", "Salary"])

    for employee in employees:
        sheet.append(
            [
                employee["name"],
                employee["department"],
                get_salary_value(employee["salary"]),
            ]
        )

    workbook.save(excel_path)

    # Read Excel file back
    read_workbook = load_workbook(excel_path, data_only=True)
    read_sheet = read_workbook.active

    row_count = read_sheet.max_row - 1

    read_workbook.close()

    return row_count


# 6. Extract first page PDF text
def extract_pdf_text() -> None:
    pdf_path = BASE_DIR / "sample.pdf"

    if not pdf_path.exists():
        logger.error("PDF file not found: sample.pdf")
        return

    with fitz.open(pdf_path) as document:
        if len(document) == 0:
            logger.error("PDF contains no pages")
            return

        text = document[0].get_text()

        print("First 100 characters of PDF:")
        print(text[:100])


# 7. Read JSON file with exception handling
def read_file(path: Union[str, Path]) -> Optional[dict]:
    file_path = Path(path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data

        logger.error("JSON file does not contain a dictionary")
        return None

    except FileNotFoundError:
        logger.error("File not found: %s", file_path.name)

    except json.JSONDecodeError:
        logger.error("Invalid JSON file: %s", file_path.name)

    return None


# 8. Find employee by name
def find_employee(name: str) -> Optional[dict]:
    # employees.json contains a list, so load it directly
    json_path = BASE_DIR / "employees.json"

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            employee_list = json.load(file)

        for employee in employee_list:
            if employee["name"].lower() == name.lower():
                return employee

    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("Unable to search employees.json")

    return None


# 9. Main program
if __name__ == "__main__":
    employees = read_employees()

    write_json(employees)

    high_count = write_high_earners(employees)

    print(f"Rows read: {len(employees)} | High earners written: {high_count}")

    excel_count = create_salary_excel(employees)

    print(f"salary.xlsx created and read back: {excel_count} rows")

    extract_pdf_text()

    # Test missing file exception
    read_file(BASE_DIR / "missing.txt")

    # Test employee search
    result = find_employee("Rahul")
    print("Employee found:", result)
