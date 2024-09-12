from fastapi.testclient import TestClient
from app.config.env import API_NAME, API_VERSION, DEFAULT_USER_NAME, DEFAULT_USER_PASSWORD
from app.app import app

client = TestClient(app)

def test_bisection():
    """
    Test the post bisection endpoint /methods/bisection/
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

    # Test with a initial value being a root
    data["expression"] = "x**2"
    data["initial"] = 0
    data["final"] = 5
    data["error_type"] = "absolute"
    data["max_iterations"] = 100
    data["tolerance"] = 0.5e-100

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/bisection/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 0
    assert answer["Xn"][-1] == "0.0"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "0"


def test_false_rule():
    """
    Test the post false rule endpoint /methods/false_rule/
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

    # Test the false rule method with a wrong interval
    data["initial"] = -1
    data["final"] = -6

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/false_rule/", json=data, headers=headers)

    assert response.status_code == 500
    answer = response.json()
    assert answer["detail"] == "La función no tiene cambio de signo en el intervalo dado"

    # Test with a initial value being a root
    data["expression"] = "x**2"
    data["initial"] = 0
    data["final"] = 5
    data["error_type"] = "absolute"
    data["max_iterations"] = 100
    data["tolerance"] = 0.5e-100

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/false_rule/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 0
    assert answer["Xn"][-1] == "0.0"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "0"


def test_fixed_point():
    """
    Test the post false rule endpoint /methods/fixed_point/
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
        "expression": "(exp(x)/x) + 3",
        "g_expression": "-(exp(x)/3)",
        "initial": -1,
        "tolerance": 0.5e-100,
        "max_iterations": 100,
        "error_type": "absolute",
        "precision": 16
    }

    # Test the fixed point method
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/fixed_point/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 30
    assert answer["Xn"][-1] == "-0.2576276530497367"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "6.938893903907228e-18"

    # Test the fixed point method with relative error
    data["error_type"] = "relative"
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/fixed_point/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 30
    assert answer["Xn"][-1] == "-0.2576276530497367"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "2.693380862561221e-17"

    # Test with a initial value being a root
    data["expression"] = "x**2"
    data["g_expression"] = "x"
    data["initial"] = 0
    data["tolerance"] = 0.5e-100
    data["max_iterations"] = 100
    data["error_type"] = "absolute"
    data["precision"] = 16

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/fixed_point/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 0
    assert answer["Xn"][-1] == "0.0"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "0"


def test_newton_raphson():
    """
    Test the post false rule endpoint /methods/newton_raphson/
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
        "expression": "(exp(x)/x) + 3",
        "initial": -1,
        "tolerance": 0.5e-100,
        "max_iterations": 100,
        "error_type": "absolute",
        "precision": 16
    }

    # Test the newton raphson method
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/newton_raphson/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 12
    assert answer["Xn"][-1] == "-0.2576276530497367"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "1.679212324745549e-15"

    # Test the newton raphson method with relative error
    data["error_type"] = "relative"
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/newton_raphson/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 12
    assert answer["Xn"][-1] == "-0.2576276530497367"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "6.517981687398155e-15"

    # Test with a initial value being a root
    data["expression"] = "x**2"
    data["initial"] = 0
    data["tolerance"] = 0.5e-100
    data["max_iterations"] = 100
    data["error_type"] = "absolute"
    data["precision"] = 16

    response = client.post(f"/api/{API_VERSION}/{API_NAME}/methods/newton_raphson/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["Iterations"][-1] == 0
    assert answer["Xn"][-1] == "0.0"
    assert answer["Fx"][-1] == "0"
    assert answer["Error"][-1] == "0"
    