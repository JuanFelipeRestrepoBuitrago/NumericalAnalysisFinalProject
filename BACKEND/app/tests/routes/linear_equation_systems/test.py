from fastapi.testclient import TestClient
from app.config.env import API_NAME, API_VERSION, DEFAULT_USER_NAME, DEFAULT_USER_PASSWORD
from app.app import app

client = TestClient(app)

def test_gauss_elimination():
    """
    Test the post gauss elimination endpoint /linear_equations_system/gauss_elimination/
    """
    # First, we need to login
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/login/", json={
        "username": DEFAULT_USER_NAME,
        "password": DEFAULT_USER_PASSWORD
    })
    assert response.status_code == 200

    # Prepare the headers
    answer = response.json()
    token = answer["access_token"]
    token_type = answer["token_type"]
    headers = {
        "Authorization": f"{token_type} {token}"
    }

    # Prepare the data
    data = {
        "A": [[3, 4, -2], [2, -3, 4], [1, -2, 3]],
        "b": [[0, 11, 7]],
        "n": 3,
        "precision": 16,
        "pivot_type": 2
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/gauss_elimination/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["x"] == [['2', '-1', '1']]
    assert answer["vectorial_error"] == [['0.0', '0.0', '0.0']]
    assert answer["absolute_error"] == '0.0'
    