from app.domain.lagrange import Lagrange
from fastapi.exceptions import HTTPException
import sympy as sp

def test_solve():
    # test 1
    x = [-2, -1]
    y = [12.13533528, 6.367879441]

    object = Lagrange(x, y, 16)
    
    expected = "0.6004236020000011 - 5.767455838999999*x"
    expected_coef = ['-5.767455838999999', '0.6004236020000011']

    result_str, result_coefficient = object.solve()

    assert result_str == expected, f"Expected: {expected}, Obtained: {result_str}"
    assert result_coefficient == expected_coef, f"Expected: {expected_coef}, Obtained: {result_coefficient}"