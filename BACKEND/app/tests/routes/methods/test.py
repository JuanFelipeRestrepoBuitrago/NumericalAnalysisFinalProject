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
        "initial": 0,
        "final": 28,
        "tolerance": 0.5e-100,
        "max_iterations": 100,
        "error_type": "absolute"
    }

    # Test the bisection method
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 55 
    assert answer["Xn"][-1] == "2.0"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "8.881784197001252e-16"

    # Test the bisection method with relative error
    data["error_type"] = "relative"
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 55
    assert answer["Xn"][-1] == "2.0"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "4.440892098500626e-16"

    # Test the bisection method with a different expression
    data["expression"] = "x**2 - 5"
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Xn"][-1] == "2.23606797749979"

    # Test the bisection method with a wrong interval
    data["initial"] = -15
    data["final"] = 5

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 500
    answer = response.json()
    assert answer["detail"] == "La función no tiene cambio de signo en el intervalo dado"

    # Test the bisection method with a wrong error type
    data["initial"] = 0
    data["final"] = 5
    data["error_type"] = "wrong"

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 422
    answer = response.json()
    assert answer["detail"][0]["msg"] == "Input should be 'absolute' or 'relative'"


def test_false_rule():
    """
    Test the post false rule endpoint /methods/false_rule/
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
        "expression": "exp(x) + 3 * cos(x)",
        "initial": -2,
        "final": -1.5,
        "tolerance": 0.5e-100,
        "max_iterations": 5,
        "error_type": "absolute"
    }

    # Test the false rule method
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/false_rule/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 5
    assert answer["Xn"][-1] == "-1.635775774845467"
    assert answer["Fx"][-1] == "-1.497813678641435e-11"
    assert answer["Error"][-1] == "8.387003036514074e-10"

    # Test the false rule method with relative error
    data["error_type"] = "relative"
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/false_rule/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 5
    assert answer["Xn"][-1] == "-1.635775774845467"
    assert answer["Fx"][-1] == "-1.497813678641435e-11"
    assert answer["Error"][-1] == "5.127232696245547e-10"

    # Test the bisection method with a wrong interval
    data["initial"] = -1
    data["final"] = -6

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/false_rule/", json=data, headers=headers)

    assert response.status_code == 500
    answer = response.json()
    assert answer["detail"] == "La función no tiene cambio de signo en el intervalo dado"

    