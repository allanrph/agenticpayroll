import requests
import json

API_KEY = "supersecretkey"
API_URL = "http://localhost:8000/calculate"
HEADERS = {"Content-Type": "application/json", "x-api-key": API_KEY}

with open("./tests/payroll_transactions.json") as file:
    employees = json.load(file)

for idx, employee_record in enumerate(employees, 1):
    response = requests.post(API_URL, headers=HEADERS, json=employee_record)

    print(response.json())
    if response.status_code == 200:
        data = response.json()

    else:
        print(f"  ❌ Error {response.status_code}: {response.text}")
