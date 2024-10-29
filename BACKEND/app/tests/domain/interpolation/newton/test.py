from app.domain.newton import Newton
from fastapi.exceptions import HTTPException
import sympy as sp

def test_create_difference_table():
    # test 1
    x = [-2, -1, 2, 3]
    y = [12.13533528, 6.367879441, -4.610943901, 2.085536923]

    object = Newton(x, y, 16)
    
    expected = sp.Matrix([
        [-2, 12.13533528, 0, 0, 0],
        [-1, 6.367879441, -5.767455838999999, 0, 0],
        [2, -4.610943901, -3.659607780666667, 0.526962014583333, 0],
        [3, 2.085536923, 6.696480824, 2.589022151166667, 0.412412027316667]
    ])

    # Check with a tolerance of 1e-15
    tolerance = 1e-15

    for i in range(4):
        for j in range(5):
            assert abs(object.difference_table[i, j] - expected[i, j]) < tolerance, f"Expected: {expected[i, j]}, Obtained: {object.difference_table[i, j]}"