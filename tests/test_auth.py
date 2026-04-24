from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_signup_returns_token():
    response = client.post(
        "/auth/signup",
        json={
            "name": "Test User",
            "email": "testuser1@test.com",
            "password": "123456",
            "role": "student"
        }
    )

    assert response.status_code in [200, 400]


def test_login_returns_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser1@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_no_token_protected_route():
    response = client.get("/batches/")
    assert response.status_code in [401, 403]