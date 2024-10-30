from app.domain.spline import Spline
from fastapi.exceptions import HTTPException
import sympy as sp

def test_solve():
    # test 1
    x = [-2, -1, 2, 3]
    y = [12.13533528, 6.367879441, -4.610943901, 2.085536923]

    object = Spline(x, y, 16)

    expected = ["0.6004236020000011 - 5.767455838999999*x", "2.708271660333334 - 3.659607780666667*x", "6.696480823999998*x - 18.003905549"]
    expected_coef = [['-5.767455838999999', '0.600423602000001'], ['-3.659607780666667', '2.708271660333334'], ['6.696480823999998', '-18.003905549']]

    result = object.solve_linear_spline()
    result_array = []
    result_coefficient_array = []

    for i in range(result.shape[0]):
        current_row = result.row(i)
        # Add elements to array with each function with the current row of the matrix
        result_array.append(object.convert_polynomial_to_string(current_row))
        result_coefficient_array.append(object.convert_1_column_matrix_to_array(current_row[0]))
        

    assert result_array == expected, f"Expected: {expected}, Obtained: {result_array}"
    assert result_coefficient_array == expected_coef, f"Expected: {expected_coef}, Obtained: {result_coefficient_array}"