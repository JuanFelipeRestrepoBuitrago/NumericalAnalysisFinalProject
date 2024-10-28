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

    