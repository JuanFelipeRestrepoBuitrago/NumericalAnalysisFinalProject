from app.domain.interpolation import Interpolation
from fastapi.exceptions import HTTPException
import sympy as sp


def test_convert_polynomial_to_string():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Interpolation(x, y)
    coefficients = sp.Matrix([1, 2, 3, 4, 5])

    result = object.convert_polynomial_to_string(coefficients)
    assert result == "5*x**4 + 4*x**3 + 3*x**2 + 2*x + 1", "Test failed for convert_polynomial_to_string"

    # test 2

    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64]

    try:
        object = Interpolation(x, y)
    except HTTPException as e:
        assert e.detail == 'El número de elementos en x debe ser igual al número de elementos en y para realizar la interpolación', "Test failed for convert_polynomial_to_string"

    # test 3

    x = [1, 2, 3, 4, 4]
    y = [1, 8, 27, 64, 125]

    try:
        object = Interpolation(x, y)
    except HTTPException as e:
        assert e.detail == 'Los valores de x deben ser únicos para realizar la interpolación, no se permiten valores repetidos', "Test failed for convert_polynomial_to_string"