from fastapi.testclient import TestClient
from app.config.env import API_NAME, API_VERSION, DEFAULT_USER_NAME, DEFAULT_USER_PASSWORD
from app.app import app

client = TestClient(app)

def test_vandermonde():
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
        "x": [-2, -1, 2, 3],
        "y": [12.13533528, 6.367879441, -4.610943901, 2.085536923],
        "precision": 16
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/interpolation/vandermonde/", json=data, headers=headers)
    expected_polynomial = "0.4124120273166665*x**3 + 0.9393740418999997*x**2 - 5.836217904516666*x + 0.004699521900001835"
    expected_coefficients = ['0.4124120273166665', '0.9393740418999997', '-5.836217904516666', '0.004699521900001835']

    assert response.status_code == 200
    answer = response.json()
    assert answer["polynomial"] == expected_polynomial, f"Expected: {expected_polynomial}, got: {answer['polynomial']}"
    assert answer["coefficients"] == expected_coefficients, f"Expected: {expected_coefficients}, got: {answer['coefficients']}"