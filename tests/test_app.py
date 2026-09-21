from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_signup_rejects_duplicate_registration():
    activity_name = "Chess Club"
    email = "duplicate-check@mergington.edu"
    activities[activity_name]["participants"] = [
        participant for participant in activities[activity_name]["participants"] if participant != email
    ]

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()


def test_unregister_participant_removes_email():
    activity_name = "Programming Class"
    email = "remove-me@mergington.edu"
    activities[activity_name]["participants"] = list(activities[activity_name]["participants"])
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
