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
    vandermonde_matrix = [['-8.00000000000000', '4.00000000000000', '-2.00000000000000', '1'], ['-1.00000000000000', '1.00000000000000', '-1.00000000000000', '1'], ['8.00000000000000', '4.00000000000000', '2.00000000000000', '1'], ['27.0000000000000', '9.00000000000000', '3.00000000000000', '1']]
    
    assert response.status_code == 200
    answer = response.json()
    assert answer["polynomial"] == expected_polynomial, f"Expected: {expected_polynomial}, got: {answer['polynomial']}"
    assert answer["coefficients"] == expected_coefficients, f"Expected: {expected_coefficients}, got: {answer['coefficients']}"
    assert answer["vandermonde_matrix"] == vandermonde_matrix, f"Expected: {vandermonde_matrix}, got: {answer['vandermonde_matrix']}"


def test_newton():
    """
    Test the post newton endpoint /interpolation/newton/
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
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/interpolation/newton/", json=data, headers=headers)
    expected_polynomial = "0.4124120273166667*x**3 + 0.9393740418999998*x**2 - 5.836217904516667*x + 0.004699521900000558"
    expected_coefficients = ['0.4124120273166667', '0.9393740418999998', '-5.836217904516667', '0.004699521900000558']
    expected_difference_table = [['-2.00000000000000', '12.1353352800000', '0', '0', '0'], ['-1.00000000000000', '6.36787944100000', '-5.767455838999999', '0', '0'], ['2.00000000000000', '-4.61094390100000', '-3.659607780666667', '0.5269620145833331', '0'], ['3.00000000000000', '2.08553692300000', '6.696480824000000', '2.589022151166667', '0.4124120273166667']]

    assert response.status_code == 200
    answer = response.json()
    assert answer["polynomial"] == expected_polynomial, f"Expected: {expected_polynomial}, got: {answer['polynomial']}"
    assert answer["coefficients"] == expected_coefficients, f"Expected: {expected_coefficients}, got: {answer['coefficients']}"
    assert answer["difference_table"] == expected_difference_table, f"Expected: {expected_difference_table}, got: {answer['difference_table']}"

def test_lagrange():
    """
    Test the post lagrange endpoint /interpolation/lagrange/
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
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/interpolation/lagrange/", json=data, headers=headers)
    expected_polynomial = "0.4124120273166666*x**3 + 0.9393740419000002*x**2 - 5.836217904516667*x + 0.004699521900000114"
    expected_coefficients = ['0.4124120273166666', '0.9393740419000002', '-5.836217904516667', '0.004699521900000114']
    expected_lagrange_polynomials = ["-0.05000000000000000*x**3 + 0.2000000000000000*x**2 - 0.05000000000000000*x - 0.3000000000000000", "0.08333333333333333*x**3 - 0.2500000000000000*x**2 - 0.3333333333333333*x + 0.9999999999999999", "-0.08333333333333333*x**3 + 0.5833333333333333*x + 0.5000000000000000", "0.05000000000000000*x**3 + 0.05000000000000000*x**2 - 0.2000000000000000*x - 0.2000000000000000"] 

    assert response.status_code == 200
    answer = response.json()
    assert answer["polynomial"] == expected_polynomial, f"Expected: {expected_polynomial}, got: {answer['polynomial']}"
    assert answer["coefficients"] == expected_coefficients, f"Expected: {expected_coefficients}, got: {answer['coefficients']}"
    assert answer["lagrange_polynomials"] == expected_lagrange_polynomials, f"Expected: {expected_lagrange_polynomials}, got: {answer['lagrange_polynomials']}"
    
    
def test_spline():
    """
    Test the post spline endpoint /interpolation/spline/
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
        "precision": 16,
        "degree": 1
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/interpolation/spline/", json=data, headers=headers)
    expected_functions = [{"function":"-5.767455838999999*x + 0.6004236020000011", "interval": "-2.0 <= x <= -1.0"}, {"function": "-3.659607780666667*x + 2.708271660333334", "interval": "-1.0 <= x <= 2.0"}, {"function": "6.696480823999998*x - 18.00390554900000",  "interval": "2.0 <= x <= 3.0"}]
    expected_coefficients = [['-5.767455838999999', '0.6004236020000011'], ['-3.659607780666667', '2.708271660333334'], ['6.696480823999998', '-18.00390554900000']]

    assert response.status_code == 200
    answer = response.json()
    assert answer["functions"] == expected_functions, f"Expected: {expected_functions}, got: {answer['functions']}"
    assert answer["coefficients"] == expected_coefficients, f"Expected: {expected_coefficients}, got: {answer['coefficients']}"
    
    data["degree"] = 3
    
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/interpolation/spline/", json=data, headers=headers)
    expected_functions = [{"function":"-0.2582814790424242*x**3 - 1.549688874254543*x**2 - 8.608552108466663*x - 0.9492652722545455", "interval": "-2.0 <= x <= -1.0"}, {"function": "0.5498827030888893*x**3 + 0.8748036721393946*x**2 - 6.184059562072727*x - 0.1411010901232310", "interval": "-1.0 <= x <= 2.0"}, {"function": "-1.391366630224242*x**3 + 12.52229967201818*x**2 - 29.47905156183031*x + 15.38889357638182",  "interval": "2.0 <= x <= 3.0"}]
    expected_coefficients = [['-0.2582814790424242', '-1.549688874254543', '-8.608552108466663', '-0.9492652722545455'], ['0.5498827030888893', '0.8748036721393946', '-6.184059562072727', '-0.1411010901232310'], ['-1.391366630224242', '12.52229967201818', '-29.47905156183031', '15.38889357638182']]
    
    assert response.status_code == 200
    answer = response.json()
    assert answer["functions"] == expected_functions, f"Expected: {expected_functions}, got: {answer['functions']}"
    assert answer["coefficients"] == expected_coefficients, f"Expected: {expected_coefficients}, got: {answer['coefficients']}"