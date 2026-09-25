import copy

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def restore_activities():
    original = {
        name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": list(details["participants"]),
        }
        for name, details in activities.items()
    }
    return original


def test_unregister_participant_removes_email_from_activity():
    original = restore_activities()
    try:
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200, response.text

        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 200, response.text
        assert email not in response.json()["participants"]
        assert email not in activities[activity_name]["participants"]
    finally:
        activities.clear()
        activities.update(original)
