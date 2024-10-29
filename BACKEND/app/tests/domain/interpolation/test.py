from app.domain.interpolation import Interpolation
from fastapi.exceptions import HTTPException
import sympy as sp


def test_convert_polynomial_to_string():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Interpolation(x, y)
    coefficients = sp.Matrix([[5], [4], [3], [2], [1]])

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

    # test 5
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Interpolation(x, y)
    coefficients = sp.Matrix([5, 4, 3, 2, 1])

    result = object.convert_polynomial_to_string(coefficients)
    assert result == "5*x**4 + 4*x**3 + 3*x**2 + 2*x + 1", "Test failed for convert_polynomial_to_string"

def test_transform_array_to_1_column_matrix():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Interpolation(x, y)
    result = object.transform_array_to_1_column_matrix(x)
    expected = sp.Matrix([[1], [2], [3], [4], [5]])
    assert result == expected, f"Got: {result}, Expected: {expected}"


def test_convert_1_column_matrix_to_array():
    # test 1
    x = [1, 2, 3, 4, 5]
    y = [1, 8, 27, 64, 125]

    object = Interpolation(x, y)
    matrix = sp.Matrix([[1], [2], [3], [4], [5]])
    result = object.convert_1_column_matrix_to_array(matrix)
    assert result == ["1", "2", "3", "4", "5"], "Test failed for convert_1_column_matrix_to_array"

def test_x_y_sorted():
    # test 1
    x = [5, 4, 3, 2, 1]
    y = [125, 64, 27, 8, 1]

    object = Interpolation(x, y)
    result = object.x
    expected = sp.Matrix([[float(i)] for i in range(1, 6)])
    assert result == expected, f"Got: {result}, Expected: {expected}"

    result = object.y
    expected = sp.Matrix([[float(i)**3] for i in range(1, 6)])
    assert result == expected, f"Got: {result}, Expected: {expected}"