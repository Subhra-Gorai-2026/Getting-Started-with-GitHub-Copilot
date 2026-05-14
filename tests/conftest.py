"""Pytest configuration and fixtures for backend tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original state of activities
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Join the school basketball team for practices and tournaments",
        "schedule": "Mondays, Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["natalie@mergington.edu", "carlos@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swim laps, improve technique, and compete in meets",
        "schedule": "Tuesdays, Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["lisa@mergington.edu", "matt@mergington.edu"]
    },
    "Art Club": {
        "description": "Create paintings, drawings, and mixed media artwork",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["anya@mergington.edu", "kyle@mergington.edu"]
    },
    "Drama Society": {
        "description": "Practice acting, stage design, and perform plays",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["amelia@mergington.edu", "dylan@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["oliver@mergington.edu", "maya@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore science experiments and discuss discoveries",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI application with reset state."""
    # Reset activities to original state before each test
    activities.clear()
    activities.update({
        key: {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy()
        }
        for key, value in ORIGINAL_ACTIVITIES.items()
    })
    return TestClient(app)
