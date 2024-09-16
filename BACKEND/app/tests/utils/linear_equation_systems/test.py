from app.utils.linear_equation_systems import GaussianElimination
from app.utils.utils import construct_augmented_matrix
from fastapi.exceptions import HTTPException
import numpy as np
from decimal import Decimal

def allclose_decimal(A, B, tol=Decimal("1e-20")):
    """
    Custom function to check if two matrices (with Decimal values) are close element-wise.
    Args:
        A: First matrix (list or np.array of Decimals)
        B: Second matrix (list or np.array of Decimals)
        tol: Tolerance level (Decimal)

    Returns:
        bool: True if all elements are close, False otherwise.
    """
    # Ensure the shapes are the same
    if A.shape != B.shape:
        return False

    # If they are vector, convert them to a (1, n) matrix to avoid errors
    if len(A.shape) == 1:
        A = A.reshape(1, -1)
    if len(B.shape) == 1:
        B = B.reshape(1, -1)

    # Compare each element in A and B with tolerance
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if abs(A[i, j] - B[i, j]) > tol:
                return False
    return True
    

def test_redefine_to_decimal():
    # test 1
    A = np.array([[1, 2], [3, 4]])
    A_decimal = np.array([[Decimal("1"), Decimal("2")], [Decimal("3"), Decimal("4")]])

    object = GaussianElimination(A, np.array([[1, 2]]), 2)
    result = object.redefine_to_decimal(A)
    assert allclose_decimal(result, A_decimal), "Test failed for a 2x2 matrix"


def test_regressive_substitution():
    # Test for a system of equations with 3 variables and the b in wrong shape
    A = np.array([[1, -2, 3], [0, 1, -2], [0, 0, 9]])
    b = np.array([7, -3, 9])
    x = np.array([[Decimal("2"), Decimal("-1"), Decimal("1")]])
    try:
        object = GaussianElimination(A, b, 3)
        AssertionError("The system of equations has the b vector in the wrong shape and should raise an exception")
    except HTTPException as e:
        assert e.detail == "Las matrices deben ser definidas con 2 paréntesis, el principal y dentro de este las filas separadas por comas. Ejemplo: [[1, 2], [3, 4]]"

    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [0, 1, -2], [0, 0, 9]])
    b = np.array([[7, -3, 9]])
    x = np.array([[Decimal("2"), Decimal("-1"), Decimal("1")]])
    object = GaussianElimination(A, b, 3)

    result = object.regressive_substitution(n=3)
    assert allclose_decimal(result, x), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
        # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [0, 3, -1, 2],
        [0, 0, 4, -2],
        [0, 0, 0, 5]
    ])
    b = np.array([[8, 9, 12, 10]])
    x = np.array([[Decimal("2.5"), Decimal("3"), Decimal("4"), Decimal("2")]])
    object = GaussianElimination(A, b, 4)

    result = object.regressive_substitution()
    assert allclose_decimal(result, x), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 5 variables
    A = np.array([
        [1, -2, 3, 0, 1],
        [0, 4, -1, 2, -3],
        [0, 0, 5, -2, 1],
        [0, 0, 0, 6, -1],
        [0, 0, 0, 0, 7]
    ])
    b = np.array([[5, 12, 17, 18, 21]])
    x = np.array([[Decimal("-1.5"), Decimal("4.55"), Decimal("4.2"), Decimal("3.5"), Decimal("3")]])
    object = GaussianElimination(A, b, 5)

    result = object.regressive_substitution()
    assert allclose_decimal(result, x), "Test failed for a system of equations with 3 variables"
    assert allclose_decimal(object.x, x), "Test failed for a system of equations with 5 variables"
    assert allclose_decimal(object.regressive_substitution(), x), "Test failed for a system of equations with 3 variables"


def test_partial_pivot():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    object = GaussianElimination(A, np.array([[7, -3, 9]]), 3)
    A_Result = np.array([[Decimal("10"), Decimal("0"), Decimal("9")], [Decimal("5"), Decimal("1"), Decimal("-2")], [Decimal("1"), Decimal("-2"), Decimal("3")]])

    result, mark = object.pivot(Ab=A, k=0, n=3, pivot_type=1)
    assert allclose_decimal(result, A_Result), "Test failed for a system of equations with 3 variables"
    assert np.allclose(mark, np.array([0, 1, 2])), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [-80, 3, -1, 2],
        [1, 0, 4, -2],
        [-8, 0, 0, 5]
    ])
    A_Result = np.array([[Decimal("-80"), Decimal("3"), Decimal("-1"), Decimal("2")], [Decimal("2"), Decimal("-1"), Decimal("0"), Decimal("3")], [Decimal("1"), Decimal("0"), Decimal("4"), Decimal("-2")], [Decimal("-8"), Decimal("0"), Decimal("0"), Decimal("5")]])
    object = GaussianElimination(A, np.array([[7, -3, 9, 0]]), 4)

    result, mark = object.pivot(Ab=A, k=0, n=4, pivot_type=1)
    assert allclose_decimal(result, A_Result), "Test failed for a system of equations with 4 variables"
    assert np.allclose(mark, np.array([0, 1, 2, 3])), "Test failed for a system of equations with 3 variables"
    

    # Test for a system of equations with 5 variables
    A = np.array([
        [1, -2, 3, 0, 1],
        [0, 4, -1, 2, -3],
        [0, 0, 5, -2, 1],
        [0, 0, 0, 6, -1],
        [0, 0, 0, 9, 7]
    ])
    A_Result = np.array([[Decimal("1"), Decimal("-2"), Decimal("3"), Decimal("0"), Decimal("1")], [Decimal("0"), Decimal("4"), Decimal("-1"), Decimal("2"), Decimal("-3")], [Decimal("0"), Decimal("0"), Decimal("5"), Decimal("-2"), Decimal("1")], [Decimal("0"), Decimal("0"), Decimal("0"), Decimal("9"), Decimal("7")], [Decimal("0"), Decimal("0"), Decimal("0"), Decimal("6"), Decimal("-1")]])
    object = GaussianElimination(A, np.array([[7, -3, 9, 0, 0]]), 5)

    result, mark = object.pivot(Ab=A, k=3, n=5, pivot_type=1)
    assert allclose_decimal(result, A_Result), "Test failed for a system of equations with 5 variables"
    assert np.allclose(mark, np.array([0, 1, 2, 3, 4])), "Test failed for a system of equations with 3 variables"

    # Test a multiple solutions system of equations
    A = np.array([
        [0, 1, 1],
        [0, 1, 1],
        [0, 1, 1]
    ])
    A_Decimal = np.array([
        [Decimal("0"), Decimal("1"), Decimal("1")],
        [Decimal("0"), Decimal("1"), Decimal("1")],
        [Decimal("0"), Decimal("1"), Decimal("1")]
    ])
    try: 
        object = GaussianElimination(A, np.array([[7, -3, 9]]), 3)

        result, mark = object.pivot(Ab=A_Decimal, k=0, n=3, pivot_type=1)
        raise AssertionError("The system of equations has multiple solutions and should raise an exception")
    except HTTPException as e:
        assert e.detail == "El sistema no tiene solución única"


def test_total_pivot():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    A_Result = np.array([[Decimal("10"), Decimal("0"), Decimal("9")], [Decimal("5"), Decimal("1"), Decimal("-2")], [Decimal("1"), Decimal("-2"), Decimal("3")]])
    object = GaussianElimination(A, np.array([[7, -3, 9]]), 3)

    result, mark = object.pivot(Ab=A, n=3, k=0, mark=np.array([0, 1, 2]), pivot_type=2)

    assert allclose_decimal(result, A_Result), "Test failed for a system of equations with 3 variables"
    assert np.allclose(mark, np.array([0, 1, 2])), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [9, 3, -1, 2],
        [1, 0, -80, -2],
        [-8, 0, 0, 5]
    ])
    A_Result = np.array([[Decimal("-80"), Decimal("0"), Decimal("1"), Decimal("-2")], [Decimal("-1"), Decimal("3"), Decimal("9"), Decimal("2")], [Decimal("0"), Decimal("-1"), Decimal("2"), Decimal("3")], [Decimal("0"), Decimal("0"), Decimal("-8"), Decimal("5")]])
    object = GaussianElimination(A, np.array([[7, -3, 9, 0]]), 4)

    result, mark = object.pivot(Ab=A, n=4, k=0, mark=np.array([0, 1, 2, 3]), pivot_type=2)

    assert allclose_decimal(result, A_Result), "Test failed for a system of equations with 4 variables"
    assert np.allclose(mark, np.array([2, 1, 0, 3])), "Test failed for a system of equations with 4 variables"

def test_organize_x():
    # Test 1
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    object = GaussianElimination(A, np.array([[7, -3, 9]]), 3)

    mark = np.array([2, 0, 1])
    x = np.array([[Decimal("2"), Decimal("-1"), Decimal("1")]])
    result = object.organize_solution(x, mark)
    assert allclose_decimal(result, np.array([[Decimal("-1"), Decimal("1"), Decimal("2")]]))

    # Test 2
    mark = np.array([2, 0, 1])
    x = np.array([[Decimal("2"), Decimal("-1"), Decimal("1")]
                  ])
    result = object.organize_solution(x, mark)
    assert allclose_decimal(result, np.array([[Decimal("-1"), Decimal("1"), Decimal("2")]]))

    # Test 3
    mark = np.array([1, 0, 2])
    x = np.array([[2, -1, 1]])
    result = object.organize_solution(x, mark)
    assert np.allclose(result, np.array([[-1, 2, 1]]))


def test_gaussian_elimination_solve():
    # Test for a system of equations with 3 variables
    A = np.array([[3, 4, -2], [2, -3, 4], [1, -2, 3]])
    object = GaussianElimination(A, np.array([[0, 11, 7]]), 3)

    x = np.array([[Decimal("2"), Decimal("-1"), Decimal("1")]])
    result = object.solve()
    zeros = object.A @ result.T - object.b.T
    A = object.A
    bT = object.b.T
    resultT = result.T
    assert allclose_decimal(result, x), "Test failed for a system of equations with 3 variables"
    assert allclose_decimal((object.A @ result.T - object.b.T).T, np.array([[Decimal("0"), Decimal("0"), Decimal("0")]])), "Test failed for a system of equations with 3 variables"

    # # Test for a system of equations with 4 variables
    # A = np.array([
    #     [2, -1, 0, 3],
    #     [8.6, 3, -1, 2],
    #     [-11.50, 3.1, 4, -2],
    #     [36.224, 3.006, 2.01, 5]
    # ])

    # object = GaussianElimination(A, np.array([[7, -3, 9, 0]]), 4, 30)
    # result = object.solve(pivot_type=2)

    # vectorial_error = A @ result.T - np.array([7, -3, 9, 0]).T

    # abs_error = np.linalg.norm(vectorial_error)

    # rest = A @ result.T - np.array([7, -3, 9, 0]).T

    # print(result)
    # print("Vectorial Error: ", )
    