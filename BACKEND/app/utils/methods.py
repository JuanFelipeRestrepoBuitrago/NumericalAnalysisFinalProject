from app.utils.utils import parse_expression, raise_exception
from app.routes.routes import logger
import sympy as sp
from typing import List, Tuple

def bisection(function: sp.Expr, variable: sp.Symbol, initial: float, final: float, tolerance: float = 0.5, iterations: int = 100, absolute_error: bool = True) -> Tuple[List[int], List[float], List[float], List[float]]:
    """
    Find the root of a function using the bisection method. The function must have a sign change in the interval [initial, final].

    Args:
        function: The function for which to find the root.
        initial: Initial value of the independent variable.
        final: Final value of the independent variable.
        tolerance: Tolerance for the root (default 0.5).
        iterations: Maximum number of iterations to perform (default 100).
        absolute_error: If True, the error is calculated as the absolute value of the difference between the current and previous values. If False, the error is calculated as the absolute value of the difference between the current and previous values divided by the current value (default True).
    Returns:
        List or table with the iterations, the values of x, the values of f(x) and the errors.
    """
    # Initialize the lists to store the function values and errors
    function_values_list = []
    values_list = []
    error_values_list = []
    counter_values_list = []
    counter = 0

    # Calculate the function values at the inprecisionitial and final points
    f_initial = function.subs(variable, initial).evalf()
    f_final = function.subs(variable, final).evalf()
    # Check if the initial or final point is a root
    if f_initial == 0:
        return [[0], [float(initial)], [float(f_initial)], [0]]
    elif f_final == 0:
        return [[0], [float(final)], [float(f_final)], [0]]
    # Check if there is a sign change in the interval [initial, final]
    
    elif f_initial * f_final > 0:
        raise_exception(ValueError("La función no tiene cambio de signo en el intervalo dado"), logger)
    else:
        # Calculate the root using the bisection method, starting with the initial and final points
        medium = (initial + final) / 2
        f_medium = function.subs(variable, medium).evalf()

        # Store values in the lists
        values_list.append(float(medium))
        function_values_list.append(float(f_medium))
        error_values_list.append(1)
        counter_values_list.append(counter + 1)

        # Iterate until the error is less than the tolerance, the function value is zero or the maximum number of iterations is reached
        while error_values_list[counter] > tolerance and f_medium != 0 and counter + 1 < iterations:
            # Check if the root is in the left or right subinterval
            if f_initial * f_medium < 0:
                final = medium
                f_final = f_medium
            else:
                initial = medium
                f_initial = f_medium

            # Temporarily store the previous medium point and calculate the new medium point
            previous_medium = medium
            medium = (initial + final) / 2
            f_medium = function.subs(variable, medium).evalf()
            function_values_list.append(float(f_medium))
            values_list.append(float(medium))

            # Calculate the error and increment the counter
            if absolute_error:
                error = abs(medium - previous_medium)
            else:
                error = abs((medium - previous_medium) / medium)
            error_values_list.append(float(error))
            counter += 1
            counter_values_list.append(counter + 1)

        # Return the list of iterations, values, function values and errors
        return [counter_values_list, values_list, function_values_list, error_values_list]
    

def false_rule(function: sp.Expr, variable: sp.Symbol, initial: float, final: float, tolerance: float = 0.5, iterations: int = 100, absolute_error: bool = True) -> Tuple[List[int], List[float], List[float], List[float]]:
    """
    Find the root of a function using the false rule method. The function must have a sign change in the interval [initial, final].

    Args:
        function: The function for which to find the root.
        initial: Initial value of the independent variable.
        final: Final value of the independent variable.
        tolerance: Tolerance for the root (default 0.5).
        iterations: Maximum number of iterations to perform (default 100).
        absolute_error: If True, the error is calculated as the absolute value of the difference between the current and previous values. If False, the error is calculated as the absolute value of the difference between the current and previous values divided by the current value (default True).
    Returns:
        List or table with the iterations, the values of x, the values of f(x) and the errors.
    """
    # Initialize the lists to store the function values and errors
    function_values_list = []
    values_list = []
    error_values_list = []
    counter_values_list = []
    counter = 0

    # Calculate the function values at the initial and final points
    f_initial = function.subs(variable, initial).evalf()
    f_final = function.subs(variable, final).evalf()
    # Check if the initial or final point is a root
    if f_initial == 0:
        return [[0], [float(initial)], [float(f_initial)], [0]]
    elif f_final == 0:
        return [[0], [float(final)], [float(f_final)], [0]]
    # Check if there is a sign change in the interval [initial, final]
    elif f_initial * f_final > 0:
        raise_exception(ValueError("La función no tiene cambio de signo en el intervalo dado"), logger)
    else:
        # Calculate the root using the false rule method, starting with the initial and final points
        medium = final - f_final * (final - initial) / (f_final - f_initial)
        f_medium = function.subs(variable, medium).evalf()

        # Store values in the lists
        values_list.append(float(medium))
        function_values_list.append(float(f_medium))
        error_values_list.append(1)
        counter_values_list.append(counter + 1)

        # Iterate until the error is less than the tolerance, the function value is zero or the maximum number of iterations is reached
        while error_values_list[counter] > tolerance and f_medium != 0 and counter + 1< iterations:
            # Check if the root is in the left or right subinterval
            if f_initial * f_medium < 0:
                final = medium
                f_final = f_medium
            else:
                initial = medium
                f_initial = f_medium

            # Temporarily store the previous medium point and calculate the new medium point
            previous_medium = medium
            medium = final - f_final * (final - initial) / (f_final - f_initial)
            f_medium = function.subs(variable, medium).evalf()
            function_values_list.append(float(f_medium))
            values_list.append(float(medium))

            # Calculate the error and increment the counter
            if absolute_error:
                error = abs(medium - previous_medium)
            else:
                error = abs((medium - previous_medium) / medium)
            error_values_list.append(float(error))
            counter += 1
            counter_values_list.append(counter + 1)

        # Return the list of iterations, values, function values and errors
        return [counter_values_list, values_list, function_values_list, error_values_list]
