from app.utils.linear_equation_systems import regressive_substitution, partial_pivot, total_pivot
from app.utils.utils import construct_augmented_matrix
from fastapi.exceptions import HTTPException
import numpy as np

def test_regressive_substitution():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [0, 1, -2], [0, 0, 9]])
    b = np.array([7, -3, 9])
    x = np.array([2, -1, 1])
    result = regressive_substitution(construct_augmented_matrix(A, b), 3)
    assert np.allclose(result, x), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
        # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [0, 3, -1, 2],
        [0, 0, 4, -2],
        [0, 0, 0, 5]
    ])
    b = np.array([8, 9, 12, 10])
    x = np.array([2.5, 3, 4, 2])
    result = regressive_substitution(construct_augmented_matrix(A, b), 4)
    assert np.allclose(result, x), "Test failed for a system of equations with 4 variables"

    # Test for a system of equations with 5 variables
    A = np.array([
        [1, -2, 3, 0, 1],
        [0, 4, -1, 2, -3],
        [0, 0, 5, -2, 1],
        [0, 0, 0, 6, -1],
        [0, 0, 0, 0, 7]
    ])
    b = np.array([5, 12, 17, 18, 21])
    x = np.array([-3/2, 91/20, 21/5, 7/2, 3])

    assert np.allclose(regressive_substitution(construct_augmented_matrix(A, b), 5), x), "Test failed for a system of equations with 5 variables"


def test_partial_pivot():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    result = partial_pivot(A, 3, 0)
    assert np.allclose(result, np.array([[10, 0, 9], [5, 1, -2], [1, -2, 3]])), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [-80, 3, -1, 2],
        [1, 0, 4, -2],
        [-8, 0, 0, 5]
    ])
    result = partial_pivot(A, 4, 0)
    assert np.allclose(result, np.array([[-80, 3, -1, 2], [2, -1, 0, 3], [1, 0, 4, -2], [-8, 0, 0, 5]])), "Test failed for a system of equations with 4 variables"

    # Test for a system of equations with 5 variables
    A = np.array([
        [1, -2, 3, 0, 1],
        [0, 4, -1, 2, -3],
        [0, 0, 5, -2, 1],
        [0, 0, 0, 6, -1],
        [0, 0, 0, 9, 7]
    ])
    result = partial_pivot(A, 5, 3)
    assert np.allclose(result, np.array([[1, -2, 3, 0, 1], [0, 4, -1, 2, -3], [0, 0, 5, -2, 1], [0, 0, 0, 9, 7], [0, 0, 0, 6, -1]])), "Test failed for a system of equations with 5 variables"

    # Test a multiple solutions system of equations
    A = np.array([
        [0, 1, 1],
        [0, 1, 1],
        [0, 1, 1]
    ])
    try: 
        result = partial_pivot(A, 3, 0)
        raise AssertionError("The system of equations has multiple solutions and should raise an exception")
    except HTTPException as e:
        assert e.detail == "El sistema no tiene solución única"


def test_total_pivot():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    result, mark = total_pivot(A, 3, 0, mark=np.array([0, 1, 2]))

    assert np.allclose(result, np.array([[10, 0, 9], [5, 1, -2], [1, -2, 3]])), "Test failed for a system of equations with 3 variables"
    assert np.allclose(mark, np.array([0, 1, 2])), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [9, 3, -1, 2],
        [1, 0, -80, -2],
        [-8, 0, 0, 5]
    ])
    result, mark = total_pivot(A, 4, 0, np.array([0, 1, 2, 3]))

    assert np.allclose(result, np.array([[-80, 0, 1, -2], [-1, 3, 9, 2], [0, -1, 2, 3], [0, 0, -8, 5]])), "Test failed for a system of equations with 4 variables"
    assert np.allclose(mark, np.array([2, 1, 0, 3])), "Test failed for a system of equations with 4 variables"
