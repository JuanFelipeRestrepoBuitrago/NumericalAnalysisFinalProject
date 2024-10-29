from app.domain.vander import Vandermonde
from fastapi.exceptions import HTTPException
import sympy as sp


def test_create_vandermonde_matrix():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Vandermonde(x, y)
    
    expected = sp.Matrix([
        [float(1), float(1), float(1), float(1), 1],
        [float(16), float(8), float(4), float(2), 1],
        [float(81), float(27), float(9), float(3), 1],
        [float(256), float(64), float(16), float(4), 1],
        [float(625), float(125), float(25), float(5), 1]
    ])
    assert object.vandermonde_matrix == expected

def test_solve():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 5]

    vandermonde = Vandermonde(x, y, precision=16)
    
    expected = 1.0e2 * sp.Matrix([
        [-0.05],
        [0.51],
        [-1.75],
        [2.5],
        [-1.2]
    ])
    
    result = vandermonde.solve()

    # Check with a tolerance for floating-point precision
    tolerance = 1e-11
    assert all(sp.Abs(a - b) <= tolerance for a, b in zip(result, expected)), f"Got: {result}, Expected: {expected}"

    # Test 2
    x = [-2, -1, 2, 3]
    y = [12.13533528, 6.367879441, -4.610943901, 2.085536923]

    vandermonde = Vandermonde(x, y, precision=16)

    expected = sp.Matrix([
        [0.412412027316666],
        [0.939374041900000],
        [-5.836217904516666],
        [0.004699521900001]
    ])

    result = vandermonde.solve()

    # Check with a tolerance for floating-point precision
    tolerance = 1e-15
    assert all(sp.Abs(a - b) <= tolerance for a, b in zip(result, expected)), f"Got: {result}, Expected: {expected}"
