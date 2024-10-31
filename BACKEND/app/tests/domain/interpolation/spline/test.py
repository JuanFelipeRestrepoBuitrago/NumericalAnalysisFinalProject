from app.domain.spline import Spline
from fastapi.exceptions import HTTPException
import sympy as sp

def test_solve():
    # test 1
    x = [-2, -1, 2, 3]
    y = [12.13533528, 6.367879441, -4.610943901, 2.085536923]

    object = Spline(x, y, 16)

    expected = ["-5.767455838999999*x + 0.6004236020000011", "-3.659607780666667*x + 2.708271660333334", "6.696480823999998*x - 18.00390554900000"]
    expected_coef = [['-5.767455838999999', '0.6004236020000011'], ['-3.659607780666667', '2.708271660333334'], ['6.696480823999998', '-18.00390554900000']]

    result = object.solve_linear_spline()
    result_array = []
    result_coefficient_array = []

    for i in range(result.shape[0]):
        current_row = result.row(i)
        # Add elements to array with each function with the current row of the matrix
        result_array.append(object.convert_coefficients_to_polynomial(current_row))
        result_coefficient_array.append(object.convert_1_n_matrix_to_array(current_row))
        

    assert result_array == expected, f"Expected: {expected}, Obtained: {result_array}"
    assert result_coefficient_array == expected_coef, f"Expected: {expected_coef}, Obtained: {result_coefficient_array}"
    
    # test 2
    
    object = Spline(x, y, 16)
    expected = [["-5.767455838999999*x + 0.6004236020000011", "-2.0 <= x <= -1.0"], ["-3.659607780666667*x + 2.708271660333334", "-1.0 <= x <= 2.0"], ["6.696480823999998*x - 18.00390554900000",  "2.0 <= x <= 3.0"]]
    result_array, result_coefficient_array = object.solve(1)
    
    assert result_array == expected, f"Expected: {expected}, Obtained: {result_array}"
    assert result_coefficient_array == expected_coef, f"Expected: {expected_coef}, Obtained: {result_coefficient_array}"
    
    # test 3
    
    object = Spline(x, y, 16)
    
    expected = ["-0.2582814790424242*x**3 - 1.549688874254543*x**2 - 8.608552108466663*x - 0.9492652722545455", "0.5498827030888893*x**3 + 0.8748036721393946*x**2 - 6.184059562072727*x - 0.1411010901232310", "-1.391366630224242*x**3 + 12.52229967201818*x**2 - 29.47905156183031*x + 15.38889357638182"]
    expected_coef = [['-0.2582814790424242', '-1.549688874254543', '-8.608552108466663', '-0.9492652722545455'], ['0.5498827030888893', '0.8748036721393946', '-6.184059562072727', '-0.1411010901232310'], ['-1.391366630224242', '12.52229967201818', '-29.47905156183031', '15.38889357638182']]
    
    result = object.solve_cubic_spline()
    
    result_array = []
    result_coefficient_array = []

    for i in range(result.shape[0]):
        current_row = result.row(i)
        # Add elements to array with each function with the current row of the matrix
        result_array.append(object.convert_coefficients_to_polynomial(current_row))
        result_coefficient_array.append(object.convert_1_n_matrix_to_array(current_row))
        

    assert result_array == expected, f"Expected: {expected}, Obtained: {result_array}"
    assert result_coefficient_array == expected_coef, f"Expected: {expected_coef}, Obtained: {result_coefficient_array}"
    
    # test 4
    
    object = Spline(x, y, 16)
    expected = [["-0.2582814790424242*x**3 - 1.549688874254543*x**2 - 8.608552108466663*x - 0.9492652722545455", "-2.0 <= x <= -1.0"], ["0.5498827030888893*x**3 + 0.8748036721393946*x**2 - 6.184059562072727*x - 0.1411010901232310", "-1.0 <= x <= 2.0"], ["-1.391366630224242*x**3 + 12.52229967201818*x**2 - 29.47905156183031*x + 15.38889357638182", "2.0 <= x <= 3.0"]]
    result_array, result_coefficient_array = object.solve(3)
    
    assert result_array == expected, f"Expected: {expected}, Obtained: {result_array}"
    assert result_coefficient_array == expected_coef, f"Expected: {expected_coef}, Obtained: {result_coefficient_array}"
    