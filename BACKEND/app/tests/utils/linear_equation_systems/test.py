from app.utils.linear_equation_systems import GaussianElimination
from app.utils.utils import construct_augmented_matrix
from fastapi.exceptions import HTTPException
import numpy as np

def test_regressive_substitution():
    # Test for a system of equations with 3 variables and the b in wrong shape
    A = np.array([[1, -2, 3], [0, 1, -2], [0, 0, 9]])
    b = np.array([7, -3, 9])
    x = np.array([2, -1, 1])
    try:
        object = GaussianElimination(A, b, 3)
        AssertionError("The system of equations has the b vector in the wrong shape and should raise an exception")
    except HTTPException as e:
        assert e.detail == "Las matrices deben ser definidas con 2 paréntesis, el principal y dentro de este las filas separadas por comas. Ejemplo: [[1, 2], [3, 4]]"

    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [0, 1, -2], [0, 0, 9]])
    b = np.array([[7, -3, 9]])
    x = np.array([2, -1, 1])
    object = GaussianElimination(A, b, 3)

    result = object.regressive_substitution(Ab=construct_augmented_matrix(A, b), n=3)
    assert np.allclose(result, x), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
        # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [0, 3, -1, 2],
        [0, 0, 4, -2],
        [0, 0, 0, 5]
    ])
    b = np.array([[8, 9, 12, 10]])
    x = np.array([2.5, 3, 4, 2])
    object = GaussianElimination(A, b, 4)

    result = object.regressive_substitution(construct_augmented_matrix(A, b), 4)
    assert np.allclose(result, x), "Test failed for a system of equations with 4 variables"

    # Test for a system of equations with 5 variables
    A = np.array([
        [1, -2, 3, 0, 1],
        [0, 4, -1, 2, -3],
        [0, 0, 5, -2, 1],
        [0, 0, 0, 6, -1],
        [0, 0, 0, 0, 7]
    ])
    b = np.array([[5, 12, 17, 18, 21]])
    x = np.array([-3/2, 91/20, 21/5, 7/2, 3])
    object = GaussianElimination(A, b, 5)

    assert np.allclose(object.regressive_substitution(construct_augmented_matrix(A, b), 5), x), "Test failed for a system of equations with 5 variables"
    assert np.allclose(object.x, x), "Test failed for a system of equations with 5 variables"
    assert np.allclose(object.regressive_substitution(), x), "Test failed for a system of equations with 5 variables"


def test_partial_pivot():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    object = GaussianElimination(A, np.array([[7, -3, 9]]), 3)

    result, mark = object.pivot(Ab=A, k=0, n=3, pivot_type=1)
    assert np.allclose(result, np.array([[10, 0, 9], [5, 1, -2], [1, -2, 3]])), "Test failed for a system of equations with 3 variables"
    assert np.allclose(mark, np.array([0, 1, 2])), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [-80, 3, -1, 2],
        [1, 0, 4, -2],
        [-8, 0, 0, 5]
    ])
    object = GaussianElimination(A, np.array([[7, -3, 9, 0]]), 4)

    result, mark = object.pivot(Ab=A, k=0, n=4, pivot_type=1)
    assert np.allclose(result, np.array([[-80, 3, -1, 2], [2, -1, 0, 3], [1, 0, 4, -2], [-8, 0, 0, 5]])), "Test failed for a system of equations with 4 variables"
    assert np.allclose(mark, np.array([0, 1, 2, 3])), "Test failed for a system of equations with 3 variables"
    

    # Test for a system of equations with 5 variables
    A = np.array([
        [1, -2, 3, 0, 1],
        [0, 4, -1, 2, -3],
        [0, 0, 5, -2, 1],
        [0, 0, 0, 6, -1],
        [0, 0, 0, 9, 7]
    ])
    object = GaussianElimination(A, np.array([[7, -3, 9, 0, 0]]), 5)

    result, mark = object.pivot(Ab=A, k=3, n=5, pivot_type=1)
    assert np.allclose(result, np.array([[1, -2, 3, 0, 1], [0, 4, -1, 2, -3], [0, 0, 5, -2, 1], [0, 0, 0, 9, 7], [0, 0, 0, 6, -1]])), "Test failed for a system of equations with 5 variables"
    assert np.allclose(mark, np.array([0, 1, 2, 3, 4])), "Test failed for a system of equations with 3 variables"

    # Test a multiple solutions system of equations
    A = np.array([
        [0, 1, 1],
        [0, 1, 1],
        [0, 1, 1]
    ])
    try: 
        object = GaussianElimination(A, np.array([[7, -3, 9]]), 3)

        result, mark = object.pivot(Ab=A, k=0, n=3, pivot_type=1)
        raise AssertionError("The system of equations has multiple solutions and should raise an exception")
    except HTTPException as e:
        assert e.detail == "El sistema no tiene solución única"


def test_pivot():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    object = GaussianElimination(A, np.array([[7, -3, 9]]), 3)

    result, mark = object.pivot(Ab=A, n=3, k=0, mark=np.array([0, 1, 2]), pivot_type=2)

    assert np.allclose(result, np.array([[10, 0, 9], [5, 1, -2], [1, -2, 3]])), "Test failed for a system of equations with 3 variables"
    assert np.allclose(mark, np.array([0, 1, 2])), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [9, 3, -1, 2],
        [1, 0, -80, -2],
        [-8, 0, 0, 5]
    ])
    object = GaussianElimination(A, np.array([[7, -3, 9, 0]]), 4)

    result, mark = object.pivot(Ab=A, n=4, k=0, mark=np.array([0, 1, 2, 3]), pivot_type=2)

    assert np.allclose(result, np.array([[-80, 0, 1, -2], [-1, 3, 9, 2], [0, -1, 2, 3], [0, 0, -8, 5]])), "Test failed for a system of equations with 4 variables"
    assert np.allclose(mark, np.array([2, 1, 0, 3])), "Test failed for a system of equations with 4 variables"
