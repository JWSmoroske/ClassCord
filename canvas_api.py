import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()

CANVAS_TOKEN = os.getenv("CANVAS_TOKEN")
CANVAS_BASE_URL = os.getenv("CANVAS_BASE_URL")

HEADERS = {"Authorization": f"Bearer {CANVAS_TOKEN}"}

def get_upcoming_assignments(days_ahead=30):
    """Fetch upcoming assignments from Canvas across all courses."""
    url = f"{CANVAS_BASE_URL}/users/self/todo" 
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error fetching assignments: {response.status_code}")
        return []
    data = response.json()
    today = datetime.now(timezone.utc)
    upcoming = []

    for item in data:
        if item.get("assignment") is None:
            continue

        assignment = item["assignment"]
        course = item.get("course", {})
        due_str = assignment.get("due_at")
        if not due_str:
            continue  # skip if no due date
        
        # ensure due date is within days ahead
        due_date = datetime.fromisoformat(due_str.replace("Z", "+00:00"))
        if today <= due_date <= today + timedelta(days=days_ahead):
            upcoming.append({
                "course_name": course.get("name", "Unknown Course"),
                "title": assignment.get("name", "No Title"),
                "due": due_date.isoformat()
            })

    return upcoming
