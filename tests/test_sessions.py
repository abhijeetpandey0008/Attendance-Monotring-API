from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def get_trainer_token():

    # Signup trainer (ignore if already exists)
    client.post(
        "/auth/signup",
        json={
            "name": "Trainer Test",
            "email": "trainer1@test.com",
            "password": "123456",
            "role": "trainer"
        }
    )

    # Login trainer
    response = client.post(
        "/auth/login",
        json={
            "email": "trainer1@test.com",
            "password": "123456"
        }
    )

    return response.json()["access_token"]


def test_trainer_create_session():

    token = get_trainer_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create batch first
    client.post(
        "/batches/",
        json={
            "name": "Test Batch",
            "description": "Batch for testing"
        },
        headers=headers
    )

    # Create session
    response = client.post(
        "/sessions/",
        json={
            "batch_id": 1,
            "title": "ML Intro",
            "date": "2026-04-25",
            "start_time": "10:00:00",
            "end_time": "11:00:00"
        },
        headers=headers
    )

    assert response.status_code in [200, 201]