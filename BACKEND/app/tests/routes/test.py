from fastapi.testclient import TestClient
from app.config.env import API_NAME, API_VERSION, DEFAULT_USER_NAME
from app.app import app

client = TestClient(app)


def test_home():
    """
    Test the home get endpoint or the root get endpoint /
    """
    response = client.get(f"/api/{API_VERSION}/{API_NAME}/")
    assert response.status_code == 200
    data = response.json()
    assert data == "Welcome to the Backend Numerical Methods API!"


def test_login():
    """
    Test the post login endpoint /login/
    """
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/login/", json={
        "username": "eafit",
        "password": "Analisis123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "Bearer"

def test_protected():
    """
    Test the get protected endpoint /protected/
    """
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/login/", json={
        "username": "eafit",
        "password": "Analisis123"
    })
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    token_type = data["token_type"]
    headers = {
        "Authorization": f"{token_type} {token}"
    }
    response = client.get(f"/api/{API_VERSION}/{API_NAME}/protected/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert f"This is a protected endpoint. Welcome, {DEFAULT_USER_NAME}!" == data

# # Test for GET /items/ endpoint
# def test_list_items():
#     response = client.get("/items/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# # Add more tests for other endpoints...