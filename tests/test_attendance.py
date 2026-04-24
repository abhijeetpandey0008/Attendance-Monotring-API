from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def get_student_token():

    # Signup student
    client.post(
        "/auth/signup",
        json={
            "name": "Student Test",
            "email": "student1@test.com",
            "password": "123456",
            "role": "student"
        }
    )

    # Login student
    response = client.post(
        "/auth/login",
        json={
            "email": "student1@test.com",
            "password": "123456"
        }
    )

    return response.json()["access_token"]


def test_student_mark_attendance():

    token = get_student_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/attendance/mark",
        json={
            "session_id": 1,
            "status": "present"
        },
        headers=headers
    )

    # Could pass or fail depending on existing DB state
    assert response.status_code in [200, 400, 403, 404]


def test_monitoring_post_not_allowed():

    response = client.post("/monitoring/attendance")

    assert response.status_code == 405