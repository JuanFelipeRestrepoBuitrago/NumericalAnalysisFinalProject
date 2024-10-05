from app.domain.gauss_seidel import GaussSeidel
from fastapi.exceptions import HTTPException
import sympy as sp


def test_iterative_solve():
    # test 1
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25, 82, 75, -43]])
    x_initial = sp.Matrix([[2, 2, 2, 2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-5)

    assert float(result[2][-1]) < 0.5e-5, "Test 1 failed for iterative_solve"
    assert result[0][-1] == 10, "Test 1 failed for iterative_solve"
    assert "0.3848001" in result[1][0][-1], "Test 1 failed for iterative_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 1 failed for iterative_solve"
    assert "1.8929358" in result[1][2][-1], "Test 1 failed for iterative_solve"
    assert "0.4700118" in result[1][3][-1], "Test 1 failed for iterative_solve"

    # test 2
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25], [82], [75], [-43]])
    x_initial = sp.Matrix([[2], [2], [2], [2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-5)
    
    assert float(result[2][-1]) < 0.5e-5, "Test 2 failed for iterative_solve"
    assert result[0][-1] == 10, "Test 2 failed for iterative_solve"
    assert "0.3848001" in result[1][0][-1], "Test 2 failed for iterative_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 2 failed for iterative_solve"
    assert "1.8929358" in result[1][2][-1], "Test 2 failed for iterative_solve"
    assert "0.4700118" in result[1][3][-1], "Test 2 failed for iterative_solve"

    # test 3
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25, 82, 75, -43]])
    x_initial = sp.Matrix([[2], [2], [2], [2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-5)

    assert float(result[2][-1]) < 0.5e-5, "Test 3 failed for iterative_solve"
    assert result[0][-1] == 10, "Test 3 failed for iterative_solve"
    assert "0.3848001" in result[1][0][-1], "Test 3 failed for iterative_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 3 failed for iterative_solve"
    assert "1.8929358" in result[1][2][-1], "Test 3 failed for iterative_solve"
    assert "0.4700118" in result[1][3][-1], "Test 3 failed for iterative_solve"

    # test 4
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25], [82], [75], [-43]])
    x_initial = sp.Matrix([[2, 2, 2, 2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.iterative_solve(0.5e-5)

    assert float(result[2][-1]) < 0.5e-5, "Test 4 failed for iterative_solve"
    assert result[0][-1] == 10, "Test 4 failed for iterative_solve"
    assert "0.3848001" in result[1][0][-1], "Test 4 failed for iterative_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 4 failed for iterative_solve"
    assert "1.8929358" in result[1][2][-1], "Test 4 failed for iterative_solve"
    assert "0.4700118" in result[1][3][-1], "Test 4 failed for iterative_solve"
    assert "es una aproximación de la solución del sistema con una tolerancia de" in result[-1], "Test 4 failed for iterative_solve"

def test_matrix_solve():
    # test 1
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25, 82, 75, -43]])
    x_initial = sp.Matrix([[2, 2, 2, 2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-5)

    assert float(result[2][-1]) < 0.5e-5, "Test 1 failed for matrix_solve"
    assert result[0][-1] == 10, "Test 1 failed for matrix_solve"
    assert "0.3848001" in result[1][0][-1], "Test 1 failed for matrix_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 1 failed for matrix_solve"
    assert "1.8929358" in result[1][2][-1], "Test 1 failed for matrix_solve"
    assert "0.4700118" in result[1][3][-1], "Test 1 failed for matrix_solve"

    # test 2
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25], [82], [75], [-43]])
    x_initial = sp.Matrix([[2], [2], [2], [2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-5)

    assert float(result[2][-1]) < 0.5e-5, "Test 2 failed for matrix_solve"
    assert result[0][-1] == 10, "Test 2 failed for matrix_solve"
    assert "0.3848001" in result[1][0][-1], "Test 2 failed for matrix_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 2 failed for matrix_solve"
    assert "1.8929358" in result[1][2][-1], "Test 2 failed for matrix_solve"
    assert "0.4700118" in result[1][3][-1], "Test 2 failed for matrix_solve"

    # test 3
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25, 82, 75, -43]])
    x_initial = sp.Matrix([[2], [2], [2], [2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-5)

    assert float(result[2][-1]) < 0.5e-5, "Test 3 failed for matrix_solve"
    assert result[0][-1] == 10, "Test 3 failed for matrix_solve"
    assert "0.3848001" in result[1][0][-1], "Test 3 failed for matrix_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 3 failed for matrix_solve"
    assert "1.8929358" in result[1][2][-1], "Test 3 failed for matrix_solve"
    assert "0.4700118" in result[1][3][-1], "Test 3 failed for matrix_solve"

    # test 4
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25], [82], [75], [-43]])
    x_initial = sp.Matrix([[2, 2, 2, 2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-5)

    assert float(result[2][-1]) < 0.5e-5, "Test 4 failed for matrix_solve"
    assert result[0][-1] == 10, "Test 4 failed for matrix_solve"
    assert "0.38480014636707" in result[1][0][-1], "Test 4 failed for matrix_solve"
    assert "-2.9618719" in result[1][1][-1], "Test 4 failed for matrix_solve"
    assert "1.8929358" in result[1][2][-1], "Test 4 failed for matrix_solve"
    assert "0.4700118" in result[1][3][-1], "Test 4 failed for matrix_solve"
    assert "es una aproximación de la solución del sistema con una tolerancia de" in result[-1], "Test 4 failed for matrix_solve"

    # test 5
    A = sp.Matrix([[45, 13, -4, 8], [-5, -28, 4, -14], [9, 15, 63, -7], [2, 3, -8, -42]])
    b = sp.Matrix([[-25], [82], [75], [-43]])
    x_initial = sp.Matrix([[2, 2, 2, 2]])

    object = GaussSeidel(A, b, x_initial, precision=16)
    result = object.matrix_solve(0.5e-5, absolute_error=False)

    assert float(result[2][-1]) < 0.5e-5, "Test 5 failed for matrix_solve"
    assert "1.3213441" in result[2][-1], "Test 5 failed for matrix_solve" 
    assert result[0][-1] == 11, "Test 5 failed for matrix_solve"
    assert "0.3847996379143" in result[1][0][-1], "Test 5 failed for matrix_solve"
    assert "-2.96187216964462" in result[1][1][-1], "Test 5 failed for matrix_solve"
    assert "1.89293601213103" in result[1][2][-1], "Test 5 failed for matrix_solve"
    assert "0.47001177785348" in result[1][3][-1], "Test 5 failed for matrix_solve"
    assert "es una aproximación de la solución del sistema con una tolerancia de" in result[-1], "Test 5 failed for iterative_solve"