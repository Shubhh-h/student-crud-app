"""Adds three dummy students. Run while the server is running: python seed.py"""
import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8000/students"

students = [
    {
        "name": "Alice Smith",
        "date_of_birth": "2001-05-20",
        "email": "alice.smith@example.com",
        "phone": "9876543210",
        "course": "Computer Science",
        "address": "Dummy Street, Test City",
        "enrollment_date": "2023-09-01",
    },
    {
        "name": "Bob Kumar",
        "date_of_birth": "2000-11-02",
        "email": "bob.kumar@example.com",
        "phone": "9123456780",
        "course": "Mathematics",
        "address": "Sample Road, Demo City",
        "enrollment_date": "2023-09-01",
    },
    {
        "name": "Priya Das",
        "date_of_birth": "2002-03-14",
        "email": "priya.das@example.com",
        "phone": "9988776655",
        "course": "Electronics",
        "address": "Test Lane, Demo Town",
        "enrollment_date": "2023-09-01",
    },
]

for s in students:
    req = urllib.request.Request(
        URL,
        data=json.dumps(s).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            print(r.status, json.loads(r.read())["name"])
    except urllib.error.HTTPError as e:
        print(e.code, s["name"], e.read().decode())
