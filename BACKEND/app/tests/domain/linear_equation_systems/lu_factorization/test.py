from app.domain.lu_factorization import LUFactorization
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

def test_progressive_substitution():
    """
    Test the progressive substitution method.
    """
    # Test for a system of equations with 3 variables and the b in wrong shape
    A = np.array([[1, -2, 3], [0, 1, -2], [0, 0, 9]])
    b = np.array([7, -3, 9])
    x = np.array([[Decimal("1"), Decimal("-1"), Decimal("2")]])
    try:
        object = LUFactorization(A, b, 3)
        AssertionError("The system of equations has the b vector in the wrong shape and should raise an exception")
    except HTTPException as e:
        assert e.detail == "Las matrices deben ser definidas con 2 paréntesis, el principal y dentro de este las filas separadas por comas. Ejemplo: [[1, 2], [3, 4]]"

    # Define the augmented matrix
    A = np.array([[9, 0, 0], [-2, 1, 0], [3, -2, 1]])
    b = np.array([[9, -3, 7]])
    x = np.array([[Decimal("1"), Decimal("-1"), Decimal("2")]])
    object = LUFactorization(A, b, 3)
    Ab = construct_augmented_matrix(object.A, object.b)

    # Perform the progressive substitution
    result = object.progressive_substitution(Ab)

    assert allclose_decimal(result, x), "Test failed for a system of equations with 3 variables"


def test_pivot():
    """
    Test the pivot method.
    """
    # Test 1
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    object = LUFactorization(A, np.array([[7, -3, 9]]), 3)
    A_Result = np.array([[Decimal("10"), Decimal("0"), Decimal("9")], [Decimal("5"), Decimal("1"), Decimal("-2")], [Decimal("1"), Decimal("-2"), Decimal("3")]])
    permutation_matrix = np.array([[Decimal("0"), Decimal("0"), Decimal("1")], [Decimal("0"), Decimal("1"), Decimal("0")], [Decimal("1"), Decimal("0"), Decimal("0")]])

    result, result_permutation_matrix = object.pivot(0, 1, Ab=object.A, n=3)
    assert allclose_decimal(result, A_Result), "Test failed for a system of equations with 3 variables"
    assert allclose_decimal(result_permutation_matrix, permutation_matrix), "Test failed for a system of equations with 3 variables"


def test_organize_matrix():
    """
    Test the organize_matrix method.
    """
        # Test 1
    A = np.array([[1, -2, 3], [5, 1, -2], [10, 0, 9]])
    object = LUFactorization(A, np.array([[7, -3, 9]]), 3)
    A_Result = np.array([[Decimal("10"), Decimal("0"), Decimal("9")], [Decimal("5"), Decimal("1"), Decimal("-2")], [Decimal("1"), Decimal("-2"), Decimal("3")]])
    permutation_matrix = np.array([[Decimal("0"), Decimal("0"), Decimal("1")], [Decimal("0"), Decimal("1"), Decimal("0")], [Decimal("1"), Decimal("0"), Decimal("0")]])

    result, result_permutation_matrix = object.pivot(0, 1, Ab=A, n=3)
    result = object.organize_matrix(A_Result, result_permutation_matrix)
    assert allclose_decimal(result, object.A)
    assert allclose_decimal(object.organize_matrix(object.b.T, result_permutation_matrix).T, np.array([[9, -3, 7]]))


def test_lu_factorization():
    # Test 1
    A = np.array([[3, 4, -2], [2, -3, 4], [1, -2, 3]])
    object = LUFactorization(A, np.array([[0, 11, 7]]), 3)


    x_expected = np.array([[Decimal("2"), Decimal("-1"), Decimal("1")]])
    
    x, L, U = object.solve()

    assert allclose_decimal(object.x, x_expected), "Test failed for a system of equations with 3 variables"
    assert allclose_decimal(L, np.array([[Decimal("1"), Decimal("0"), Decimal("0")], [Decimal("2")/Decimal("3"), Decimal("1"), Decimal("0")], [Decimal("1")/Decimal("3"), Decimal("0.5882352941176470"), Decimal("1")]]))
    assert allclose_decimal(U, np.array([[Decimal("3"), Decimal("4"), Decimal("-2")], [Decimal("0"), Decimal("-5.666666666666667"), Decimal("5.333333333333333")], [Decimal("0"), Decimal("0"), Decimal("0.529411764705883")]]))
    assert allclose_decimal(object.get_set_vectorial_error(x, object.A, object.b), np.array([[Decimal("0"), Decimal("0"), Decimal("0")]])), "Test failed for a system of equations with 3 variables"
    assert object.get_set_absolute_error(object.get_set_vectorial_error(x, object.A, object.b)) == 0, "Test failed for a system of equations with 3 variables"

    # Test 2
    # A = [4 3 2 1;3 12 3 -2; -2 8 -9 -5; -7 -3 3 6];
    # b = [0;8;7;1];
    A = np.array([[4, 3, 2, 1], [3, 12, 3, -2], [-2, 8, -9, -5], [-7, -3, 3, 6]])
    object = LUFactorization(A, np.array([[0, 8, 7, 1]]), 4)
    x_expected = np.array([[Decimal("-0.5743319533308244"), Decimal("0.7485886337975161"), Decimal("0.1204365826119690"), Decimal("-0.1893112532931884")]])
    L_expected = np.array([[Decimal("1"), Decimal("0"), Decimal("0"), Decimal("0")], [Decimal("-0.4285714285714286"), Decimal("1"), Decimal("0"), Decimal("0")], [Decimal("0.2857142857142857"), Decimal('0.8266666666666670'), Decimal("1"), Decimal("0")], [Decimal("-0.5714285714285714"), Decimal('0.1200000000000001'), Decimal("-0.2388059701492537"), Decimal("1")]])
    U_expected = np.array([[Decimal("-7.000000000000000"), Decimal("-3.000000000000000"), Decimal("3.000000000000000"), Decimal("6.000000000000000")], [Decimal("0"), Decimal("10.71428571428571"), Decimal("4.285714285714286"), Decimal("0.571428571428572")], [Decimal("0"), Decimal("0"), Decimal("-13.400000000000000"), Decimal("-7.186666666666667")], [Decimal("0"), Decimal("0"), Decimal("0"), Decimal("2.643781094527362")]])

    x, L, U = object.solve(pivot_type=1)
    object.get_set_vectorial_error()
    object.get_set_absolute_error()

    assert allclose_decimal(object.x, x_expected), "Test failed for a system of equations with 4 variables"
    assert allclose_decimal(L, L_expected)
    assert allclose_decimal(U, U_expected)
