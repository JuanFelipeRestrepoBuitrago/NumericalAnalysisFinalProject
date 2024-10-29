from app.domain.vander import Vandermonde
from fastapi.exceptions import HTTPException
import sympy as sp


def test_create_vandermonde_matrix():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Vandermonde(x, y)
    
    expected = sp.Matrix([
        [1, 1, 1, 1, 1],
        [16, 8, 4, 2, 1],
        [81, 27, 9, 3, 1],
        [256, 64, 16, 4, 1],
        [625, 125, 25, 5, 1]
    ])
    assert object.vandermonde_matrix == expected

def test_solve():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Vandermonde(x, y, 17)
    
    expected = sp.Matrix([
        [-0.000000000000001],
        [1.000000000000014],
        [0.000000000000028],
        [-0.000000000000057],
        [0.000000000000014]
    ])
    result = object.solve()
    assert  result == expected

    # test 2
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Vandermonde(x, y)
    
    expected = sp.Matrix([
        [1],
        [1],
        [1],
        [1],
        [1]
    ])
    assert object.solve(object.vandermonde_matrix, object.y) == expected

    