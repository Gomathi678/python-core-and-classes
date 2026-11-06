
import csv
from pathlib import Path
from functools import wraps


# 1. Function with default values, *args and **kwargs

def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


# 2. Decorator

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# 3. Employee class

class Employee:

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"Employee Name: {self.name}, Salary: Rs.{self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


# 4. Manager class using inheritance

class Manager(Employee):

    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return (
            f"Manager Name: {self.name}, "
            f"Salary: Rs.{self.salary}, "
            f"Team Size: {self.team_size}"
        )


# 5. Read employee data from CSV using pathlib

def read_employees():
    file_path = Path(__file__).parent / "employees.csv"

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for employee in reader:
            print(employee)


# 6. Main program

if __name__ == "__main__":

    print("===== BONUS CALCULATION =====")

    bonus = calculate_bonus(30000)
    print("Bonus:", bonus)

    bonus = calculate_bonus(30000, 0.1, 500, 1000, cap=3500)
    print("Bonus with extras and cap:", bonus)

    print("\n===== EMPLOYEE DETAILS =====")

    emp = Employee("Arun", 30000)

    print(emp.get_details())
    print("Annual Salary:", emp.annual_salary)

    print("\n===== MANAGER DETAILS =====")

    manager = Manager("Priya", 60000, 5)

    print(manager.get_details())

    print("\n===== EMPLOYEES CSV DATA =====")

    read_employees()
