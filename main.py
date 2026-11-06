

import csv
from pathlib import Path
from functools import wraps


# 1. Calculate bonus using *args and **kwargs

def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# 2. Decorator

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Calling get_details")
        return func(*args, **kwargs)

    return wrapper


# 3. Employee class

class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# 4. Manager class with inheritance

class Manager(Employee):

    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


# 5. Read CSV and categorize salaries

def salary_categories():

    file_path = Path(__file__).parent / "employees.csv"

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for employee in reader:

            name = employee["name"]
            salary = int(employee["salary"])

            if salary < 50000:
                category = "Low Salary"

            elif salary < 70000:
                category = "Medium Salary"

            else:
                category = "High Salary"

            print(f"{name} - {category}")


# 6. Main program

if __name__ == "__main__":

    print("===== SALARY CATEGORIES =====")
    salary_categories()

    print("\n===== MANAGER DETAILS =====")

    manager = Manager("Divya", 75000, 5)
    print(manager.get_details())

    print("\n===== BONUS CALCULATION =====")

    print("Bonus:", calculate_bonus(30000))
    print(
        "Bonus with extras and cap:",
        calculate_bonus(30000, 0.1, 500, 1000, cap=3500)
    )

    print("\n===== ANNUAL SALARY =====")

    emp = Employee("Arun", 30000)
    print(emp.annual_salary)
