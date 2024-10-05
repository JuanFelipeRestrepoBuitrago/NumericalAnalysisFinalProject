from app.domain.jacobi import Jacobi
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
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    A_decimal = np.array([[Decimal("45"), Decimal("13"), Decimal("-4"), Decimal("8")], [Decimal("-5"), Decimal("-28"), Decimal("4"), Decimal("-14")], [Decimal("9"), Decimal("15"), Decimal("63"), Decimal("-7")], [Decimal("2"), Decimal("3"), Decimal("-8"), Decimal("-42")]])

    object = Jacobi(A, np.array([[-25, 82, 75, -43]]), np.array([[2, 2, 2, 2]]), precision=16)
    result = object.redefine_to_decimal(A)
    assert allclose_decimal(result, A_decimal), "Test failed for a 2x2 matrix"


def test_iterative_solve():
    # test 1
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25, 82, 75, -43]])
    x_initial = np.array([[2, 2, 2, 2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-4)

    assert result[1][1][1] == "-4", "Test 1 failed for iterative_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 1 failed for iterative_solve"
    assert result[0][-1] == 12, "Test 1 failed for iterative_solve"
    assert "0.38480376" in result[1][0][-1], "Test 1 failed for iterative_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 1 failed for iterative_solve"
    assert "1.8929326" in result[1][2][-1], "Test 1 failed for iterative_solve"
    assert "0.4700089" in result[1][3][-1], "Test 1 failed for iterative_solve"

    # test 2
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25], [82], [75], [-43]])
    x_initial = np.array([[2], [2], [2], [2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-4)
    
    assert result[1][1][1] == "-4", "Test 2 failed for iterative_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 2 failed for iterative_solve"
    assert result[0][-1] == 12, "Test 2 failed for iterative_solve"
    assert "0.38480376" in result[1][0][-1], "Test 2 failed for iterative_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 2 failed for iterative_solve"
    assert "1.8929326" in result[1][2][-1], "Test 2 failed for iterative_solve"
    assert "0.4700089" in result[1][3][-1], "Test 2 failed for iterative_solve"

    # test 3
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25, 82, 75, -43]])
    x_initial = np.array([[2], [2], [2], [2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-4)

    assert result[1][1][1] == "-4", "Test 3 failed for iterative_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 3 failed for iterative_solve"
    assert result[0][-1] == 12, "Test 3 failed for iterative_solve"
    assert "0.38480376" in result[1][0][-1], "Test 3 failed for iterative_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 3 failed for iterative_solve"
    assert "1.8929326" in result[1][2][-1], "Test 3 failed for iterative_solve"
    assert "0.4700089" in result[1][3][-1], "Test 3 failed for iterative_solve"

    # test 4
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25], [82], [75], [-43]])
    x_initial = np.array([[2, 2, 2, 2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-4)

    assert result[1][1][1] == "-4", "Test 4 failed for iterative_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 4 failed for iterative_solve"
    assert result[0][-1] == 12, "Test 4 failed for iterative_solve"
    assert "0.38480376" in result[1][0][-1], "Test 4 failed for iterative_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 4 failed for iterative_solve"
    assert "1.8929326" in result[1][2][-1], "Test 4 failed for iterative_solve"
    assert "0.4700089" in result[1][3][-1], "Test 4 failed for iterative_solve"

    # test 5
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25], [82], [75], [-43]])
    x_initial = np.array([[2, 2, 2, 2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-4, absolute_error=False)

    assert "-4" in result[1][1][1], "Test 5 failed for iterative_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 5 failed for iterative_solve"
    assert "0.000027324160930" in result[2][-1], "Test 5 failed for iterative_solve" 
    assert result[0][-1] == 12, "Test 5 failed for iterative_solve"
    assert "0.38480376" in result[1][0][-1], "Test 5 failed for iterative_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 5 failed for iterative_solve"
    assert "1.8929326" in result[1][2][-1], "Test 5 failed for iterative_solve"
    assert "0.4700089" in result[1][3][-1], "Test 5 failed for iterative_solve"
    assert "es una aproximación de la solución del sistema con una tolerancia de" in result[-1], "Test 5 failed for iterative_solve"

def test_matrix_solve():
    # test 1
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25, 82, 75, -43]])
    x_initial = np.array([[2, 2, 2, 2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-4)

    assert "-4" in result[1][1][1], "Test 4 failed for matrix_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 1 failed for matrix_solve"
    assert result[0][-1] == 12, "Test 1 failed for matrix_solve"
    assert "0.38480376" in result[1][0][-1], "Test 1 failed for matrix_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 1 failed for matrix_solve"
    assert "1.8929326" in result[1][2][-1], "Test 1 failed for matrix_solve"
    assert "0.4700089" in result[1][3][-1], "Test 1 failed for matrix_solve"

    # test 2
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25], [82], [75], [-43]])
    x_initial = np.array([[2], [2], [2], [2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-4)
    
    assert "-4" in result[1][1][1], "Test 4 failed for matrix_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 2 failed for matrix_solve"
    assert result[0][-1] == 12, "Test 2 failed for matrix_solve"
    assert "0.38480376" in result[1][0][-1], "Test 2 failed for matrix_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 2 failed for matrix_solve"
    assert "1.8929326" in result[1][2][-1], "Test 2 failed for matrix_solve"
    assert "0.4700089" in result[1][3][-1], "Test 2 failed for matrix_solve"

    # test 3
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25, 82, 75, -43]])
    x_initial = np.array([[2], [2], [2], [2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-4)

    assert "-4" in result[1][1][1], "Test 4 failed for matrix_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 3 failed for matrix_solve"
    assert result[0][-1] == 12, "Test 3 failed for matrix_solve"
    assert "0.38480376" in result[1][0][-1], "Test 3 failed for matrix_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 3 failed for matrix_solve"
    assert "1.8929326" in result[1][2][-1], "Test 3 failed for matrix_solve"
    assert "0.4700089" in result[1][3][-1], "Test 3 failed for matrix_solve"

    # test 4
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25], [82], [75], [-43]])
    x_initial = np.array([[2, 2, 2, 2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-4)

    assert "-4" in result[1][1][1], "Test 4 failed for matrix_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 4 failed for matrix_solve"
    assert result[0][-1] == 12, "Test 4 failed for matrix_solve"
    assert "0.38480376" in result[1][0][-1], "Test 4 failed for matrix_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 4 failed for matrix_solve"
    assert "1.8929326" in result[1][2][-1], "Test 4 failed for matrix_solve"
    assert "0.4700089" in result[1][3][-1], "Test 4 failed for matrix_solve"

    # test 5
    A = np.array([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = np.array([[-25], [82], [75], [-43]])
    x_initial = np.array([[2, 2, 2, 2]])

    object = Jacobi(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-4, absolute_error=False)

    assert "-4" in result[1][1][1], "Test 5 failed for matrix_solve"
    assert float(result[2][-1]) < 0.5e-4, "Test 5 failed for matrix_solve"
    assert "2.73241609" in result[2][-1], "Test 5 failed for matrix_solve" 
    assert result[0][-1] == 12, "Test 5 failed for matrix_solve"
    assert "0.38480376" in result[1][0][-1], "Test 5 failed for matrix_solve"
    assert "-2.96186574" in result[1][1][-1], "Test 5 failed for matrix_solve"
    assert "1.8929326" in result[1][2][-1], "Test 5 failed for matrix_solve"
    assert "0.4700089" in result[1][3][-1], "Test 5 failed for matrix_solve"
    assert "es una aproximación de la solución del sistema con una tolerancia de" in result[-1], "Test 5 failed for iterative_solve"