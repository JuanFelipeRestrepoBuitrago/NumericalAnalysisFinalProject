from fastapi.testclient import TestClient
from app.config.env import API_NAME, API_VERSION, DEFAULT_USER_NAME
from app.app import app

client = TestClient(app)

def test_bisection():
    """
    Test the post bisection endpoint /methods/bisection/
    """
    # First, we need to login
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/login/", json={
        "username": "eafit",
        "password": "Analisis123"
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
        "expression": "x**2 - 4",
        "a": 0,
        "b": 28,
        "tolerance": 0.5e-100,
        "max_iterations": 100,
        "error_type": "absolute"
    }

    # Test the bisection method
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 55 
    assert answer["Xn"][-1] == 2
    assert answer["Fx"][-1] == 0
    assert answer["Error"][-1] == 8.881784197001252e-16

    # Test the bisection method with relative error
    data["error_type"] = "relative"
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 55
    assert answer["Xn"][-1] == 2
    assert answer["Fx"][-1] == 0
    assert answer["Error"][-1] == 4.440892098500626e-16

    # Test the bisection method with a different expression
    data["expression"] = "x**2 - 5"
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Xn"][-1] == 2.23606797749978980505

    # Test the bisection method with a wrong interval
    data["a"] = -15
    data["b"] = 5

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 500
    answer = response.json()
    assert answer["detail"] == "La función no tiene cambio de signo en el intervalo dado"

    