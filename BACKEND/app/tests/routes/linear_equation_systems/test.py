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

def test_lu_factorization():
    """
    Test the post lu factorization endpoint /linear_equations_system/lu_factorization/
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
        "n": 3
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/lu_factorization/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["x"] == [['2', '-1', '1']]
    assert answer["L"] == [['1.0', '0.0', '0.0'], ['0.6666666666666667', '1.0', '0.0'], ['0.3333333333333333', '0.5882352941176470', '1.0']]
    assert answer["U"] == [['3.0', '4.0', '-2.0'], ['0.0', '-5.666666666666667', '5.333333333333333'], ['0.0', '0.0', '0.529411764705883']]
    assert answer["vectorial_error"] == [['0.0', '0.0', '0.0']]
    assert answer["absolute_error"] == "0.0"

def test_jacobi():
    """
    Test the post lu factorization endpoint /linear_equations_system/jacobi/
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
        "A": [[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]],
        "b": [[-25], [82], [75], [-43]],
        "x_initial": [[2], [2], [2], [2]],
        "tol": 0.5e-4,
        "max_iter": 100,
        "order": 0,
        "precision": 16,
        "method_type": "iterative"
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/jacobi/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["iterations"][-1] == 12
    assert "0.38480376" in answer["x"][0][12]
    assert "-2.96186574" in answer["x"][1][12]
    assert "1.8929326" in answer["x"][2][12]
    assert "0.4700089" in answer["x"][3][12]
    assert "es una aproximación de la solución del sistema con una tolerancia de" in answer["message"]

    # Test 2
    data["method_type"] = "matrix"

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/jacobi/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()

    assert answer["iterations"][-1] == 12
    assert "0.38480376" in answer["x"][0][12]
    assert "-2.96186574" in answer["x"][1][12]
    assert "1.8929326" in answer["x"][2][12]
    assert "0.4700089" in answer["x"][3][12]
    assert "es una aproximación de la solución del sistema con una tolerancia de" in answer["message"]

def test_gauss_seidel():
    """
    Test the post lu factorization endpoint /linear_equations_system/gauss_seidel/
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
        "A": [[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]],
        "b": [[-25], [82], [75], [-43]],
        "x_initial": [[2], [2], [2], [2]],
        "tol": 0.5e-5,
        "max_iter": 100,
        "order": 0,
        "precision": 16,
        "method_type": "iterative"
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/gauss_seidel/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["iterations"][-1] == 10
    assert "0.3848001" in answer["x"][0][10]
    assert "-2.9618719" in answer["x"][1][10]
    assert "1.8929358" in answer["x"][2][10]
    assert "0.4700118" in answer["x"][3][10]
    assert "es una aproximación de la solución del sistema con una tolerancia de" in answer["message"]

    # Test 2
    data["method_type"] = "matrix"

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/gauss_seidel/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()

    assert answer["iterations"][-1] == 10
    assert "0.38480014636707" in answer["x"][0][10]
    assert "-2.9618719" in answer["x"][1][10]
    assert "1.8929358" in answer["x"][2][10]
    assert "0.4700118" in answer["x"][3][10]
    assert "es una aproximación de la solución del sistema con una tolerancia de" in answer["message"]


def test_sor():
    """
    Test the post lu factorization endpoint /linear_equations_system/sor/
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
        "A": [[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]],
        "b": [[-25], [82], [75], [-43]],
        "x_initial": [[2], [2], [2], [2]],
        "tol": 0.5e-5,
        "max_iter": 100,
        "order": 0,
        "precision": 16,
        "method_type": "iterative",
        "w": 1.001
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/sor/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert answer["iterations"][-1] == 10
    assert "0.3848001" in answer["x"][0][10]
    assert "-2.9618719" in answer["x"][1][10]
    assert "1.8929358" in answer["x"][2][10]
    assert "0.4700118" in answer["x"][3][10]
    assert "es una aproximación de la solución del sistema con una tolerancia de" in answer["message"]

    # Test 2
    data["method_type"] = "matrix"

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/sor/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()

    assert answer["iterations"][-1] == 10
    assert "0.38480019183067" in answer["x"][0][10]
    assert "-2.96187191357149" in answer["x"][1][10]
    assert "1.89293582381225" in answer["x"][2][10]
    assert "0.47001185882341" in answer["x"][3][10]
    assert "es una aproximación de la solución del sistema con una tolerancia de" in answer["message"]


def test_jacobi_spectral_radius_and_convergence():
    """
    Test the post lu factorization endpoint /linear_equations_system/jacobi/spectral_radius_and_convergence/
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
        "A": [[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]],
        "b": [[-25], [82], [75], [-43]],
        "x_initial": [[2], [2], [2], [2]],
        "tol": 0.5e-4,
        "max_iter": 100,
        "order": 0,
        "precision": 16,
        "method_type": "iterative"
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/jacobi/spectral_radius_and_convergence/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert "0.33974160954560" in answer["spectral_radius"]
    assert answer["convergence"] == "El método converge, el radio espectral de T es menor a 1 y/o la matriz es estrictamente diagonal dominante"


def test_gauss_seidel_spectral_radius_and_convergence():
    """
    Test the post lu factorization endpoint /linear_equations_system/gauss_seidel/spectral_radius_and_convergence/
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
        "A": [[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]],
        "b": [[-25], [82], [75], [-43]],
        "x_initial": [[2], [2], [2], [2]],
        "tol": 0.5e-5,
        "max_iter": 100,
        "order": 0,
        "precision": 16,
        "method_type": "iterative"
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/gauss_seidel/spectral_radius_and_convergence/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert "0.18881517244860" in answer["spectral_radius"]
    assert answer["convergence"] == "El método converge, el radio espectral de T es menor a 1 y/o la matriz es estrictamente diagonal dominante"

def test_sor_spectral_radius_and_convergence():
    """
    Test the post lu factorization endpoint /linear_equations_system/sor/spectral_radius_and_convergence/
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
        "A": [[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]],
        "b": [[-25], [82], [75], [-43]],
        "x_initial": [[2], [2], [2], [2]],
        "tol": 0.5e-5,
        "max_iter": 100,
        "order": 0,
        "precision": 16,
        "method_type": "iterative",
        "w": 1.001
    }

    # Make the request
    response = client.post(f"/api/{API_VERSION}/{API_NAME}/linear_equations_system/sor/spectral_radius_and_convergence/", json=data, headers=headers)

    assert response.status_code == 200
    answer = response.json()
    assert "0.19091650493849" in answer["spectral_radius"]
    assert answer["convergence"] == "El método converge, el radio espectral de T es menor a 1 y/o la matriz es estrictamente diagonal dominante"
    