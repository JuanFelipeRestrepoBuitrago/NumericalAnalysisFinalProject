from app.utils.utils import parse_expression, raise_exception
from app.routes.routes import logger
import sympy as sp
from typing import List, Tuple

def bisection(function: sp.Expr, variable: sp.Symbol, initial: float, final: float, tolerance: float = 0.5, iterations: int = 100, absolute_error: bool = True, precision: int = 16) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Find the root of a function using the bisection method. The function must have a sign change in the interval [initial, final].

    Args:
        function: The function for which to find the root.
        initial: Initial value of the independent variable.
        final: Final value of the independent variable.
        tolerance: Tolerance for the root (default 0.5).
        iterations: Maximum number of iterations to perform (default 100).
        absolute_error: If True, the error is calculated as the absolute value of the difference between the current and previous values. If False, the error is calculated as the absolute value of the difference between the current and previous values divided by the current value (default True).
        precision: Number of decimal places to round the values (default 15).
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
    f_initial = function.subs(variable, initial).evalf(precision)
    f_final = function.subs(variable, final).evalf(precision)
    # Check if the initial or final point is a root
    if f_initial == 0:
        return [[0], [str(initial)], [str(f_initial)], ["0"]]
    elif f_final == 0:
        return [[0], [str(final)], [str(f_final)], ["0"]]
    # Check if there is a sign change in the interval [initial, final]
    
    elif f_initial * f_final > 0:
        raise_exception(ValueError("La función no tiene cambio de signo en el intervalo dado"), logger)
    else:
        # Calculate the root using the bisection method, starting with the initial and final points
        medium = (initial + final) / 2
        f_medium = function.subs(variable, medium).evalf(precision)

        # Store values in the lists
        values_list.append(str(medium))
        function_values_list.append(str(f_medium))
        error_values_list.append(str(1))
        counter_values_list.append(counter + 1)
        previous_error = 1

        # Iterate until the error is less than the tolerance, the function value is zero or the maximum number of iterations is reached
        while previous_error > tolerance and f_medium != 0 and counter + 1 < iterations:
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
            f_medium = function.subs(variable, medium).evalf(precision)
            function_values_list.append(str(f_medium))
            values_list.append(str(medium))

            # Calculate the error and increment the counter
            if absolute_error:
                error = abs(medium - previous_medium)
            else:
                error = abs((medium - previous_medium) / medium)
            error_values_list.append(str(error))
            previous_error = error
            counter += 1
            counter_values_list.append(counter + 1)

        # Return the list of iterations, values, function values and errors
        return [counter_values_list, values_list, function_values_list, error_values_list]
    

def false_rule(function: sp.Expr, variable: sp.Symbol, initial: float, final: float, tolerance: float = 0.5, iterations: int = 100, absolute_error: bool = True, precision: int = 16) -> Tuple[List[int], List[str], List[str], List[str]]:
    """
    Find the root of a function using the false rule method. The function must have a sign change in the interval [initial, final].

    Args:
        function: The function for which to find the root.
        initial: Initial value of the independent variable.
        final: Final value of the independent variable.
        tolerance: Tolerance for the root (default 0.5).
        iterations: Maximum number of iterations to perform (default 100).
        absolute_error: If True, the error is calculated as the absolute value of the difference between the current and previous values. If False, the error is calculated as the absolute value of the difference between the current and previous values divided by the current value (default True).
        precision: Number of decimal places to round the values (default 15).
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
    f_initial = function.subs(variable, initial).evalf(precision)
    f_final = function.subs(variable, final).evalf(precision)
    # Check if the initial or final point is a root
    if f_initial == 0:
        return [[0], [str(initial)], [str(f_initial)], ["0"]]
    elif f_final == 0:
        return [[0], [str(final)], [str(f_final)], ["0"]]
    # Check if there is a sign change in the interval [initial, final]
    elif f_initial * f_final > 0:
        raise_exception(ValueError("La función no tiene cambio de signo en el intervalo dado"), logger)
    else:
        # Calculate the root using the false rule method, starting with the initial and final points
        medium = final - f_final * (final - initial) / (f_final - f_initial)
        f_medium = function.subs(variable, medium).evalf(precision)

        # Store values in the lists
        values_list.append(str(medium))
        function_values_list.append(str(f_medium))
        error_values_list.append(str(1))
        counter_values_list.append(counter + 1)
        previous_error = 1

        # Iterate until the error is less than the tolerance, the function value is zero or the maximum number of iterations is reached
        while previous_error > tolerance and f_medium != 0 and counter + 1< iterations:
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
            f_medium = function.subs(variable, medium).evalf(precision)
            function_values_list.append(str(f_medium))
            values_list.append(str(medium))

            # Calculate the error and increment the counter
            if absolute_error:
                error = abs(medium - previous_medium)
            else:
                error = abs((medium - previous_medium) / medium)
            error_values_list.append(str(error))
            previous_error = error
            counter += 1
            counter_values_list.append(counter + 1)

        # Return the list of iterations, values, function values and errors
        return [counter_values_list, values_list, function_values_list, error_values_list]
    

def fixed_point(function: sp.Expr, variable: sp.Symbol, g_function: sp.Expr, initial_value: float, tolerance: float = 0.5, iterations: int = 100, absolute_error: bool = True, precision: int = 16) -> Tuple[List[int], List[str], List[str], List[str]]:
    """
    Find the root of a function using the fixed point method.
    
    Args:
        function: The function for which to find the root.
        g_function: The function to use in the fixed point method.
        initial_value: Initial value of the independent variable.
        tolerance: Tolerance for the root (default 0.5).
        iterations: Maximum number of iterations to perform (default 100).
        absolute_error: If True, the error is calculated as the absolute value of the difference between the current and previous values. If False, the error is calculated as the absolute value of the difference between the current and previous values divided by the current value (default True).
        precision: Number of decimal places to round the values (default 15).
    Returns:
        List or table with the iterations, the values of x, the values of f(x) and the errors.
    """
    # Initialize the lists to store the function values and errors
    function_values_list = []
    values_list = []
    error_values_list = []
    counter_values_list = []
    counter = 0

    # Calculate the function value at the initial point
    f_initial = function.subs(variable, initial_value).evalf(precision)

    # Check if the initial point is a root
    if f_initial == 0:
        return [[0], [str(initial_value)], [str(f_initial)], ["0"]]
    else:
        # Set the variables needed for the iterations
        x = initial_value
        f_x = f_initial
        # Initialize the error
        previous_error = 1

        # Add the initial values to the lists
        values_list.append(str(x))
        function_values_list.append(str(f_x))
        error_values_list.append(str(previous_error))
        counter_values_list.append(counter)

        # Iterate until the error is less than the tolerance, the function value is zero or the maximum number of iterations is reached
        while previous_error > tolerance and f_x != 0 and counter < iterations:
            # Sets the previous x value
            x_previous = x

            # Calculate the new value of x using the g function
            x = g_function.subs(variable, x).evalf(precision)
            f_x = function.subs(variable, x).evalf(precision)

            # Store the values in the lists
            values_list.append(str(x))
            function_values_list.append(str(f_x))

            # Calculate the error and increment the counter
            if absolute_error: 
                error = abs(x - x_previous)
            else:
                error = abs((x - x_previous) / x)
            counter += 1

            # Store the error in the list, update the previous error and add the counter to the list
            error_values_list.append(str(error))
            previous_error = error
            counter_values_list.append(counter)

        # Return the list of iterations, values, function values and errors
        return [counter_values_list, values_list, function_values_list, error_values_list]
    

def newton_raphson(function: sp.Expr, variable: sp.Symbol, initial: float, derivative: sp.Expr = None, tolerance: float = 0.5, iterations: int = 100, absolute_error: bool = True, precision: int = 16) -> Tuple[List[int], List[str], List[str], List[str]]:
    """
    Find the root of a function using the Newton-Raphson method.
    
    Args:
        function: The function for which to find the root.
        initial: Initial value of the independent variable.
        derivative: The derivative of the function (default None).
        tolerance: Tolerance for the root (default 0.5).
        iterations: Maximum number of iterations to perform (default 100).
        absolute_error: If True, the error is calculated as the absolute value of the difference between the current and previous values. If False, the error is calculated as the absolute value of the difference between the current and previous values divided by the current value (default True).
        precision: Number of decimal places to round the values (default 15).
    Returns:
        List or table with the iterations, the values of x, the values of f(x) and the errors.
    """
    # Initialize the lists to store the function values and errors
    function_values_list = []
    values_list = []
    error_values_list = []
    counter_values_list = []
    counter = 0

    # Calculate the function value at the initial point
    f_initial = function.subs(variable, initial).evalf(precision)

    # Check if the initial point is a root
    if f_initial == 0:
        return [[0], [str(initial)], [str(f_initial)], ["0"]]
    else:
        # Set the variables needed for the iterations
        x = initial
        f_x = f_initial
        # Initialize the error
        previous_error = 1

        # Add the initial values to the lists
        values_list.append(str(x))
        function_values_list.append(str(f_x))
        error_values_list.append(str(previous_error))
        counter_values_list.append(counter)

        # Calculate the derivative of the function if it is not provided
        if derivative is None:
            derivative = sp.diff(function, variable)

        # Iterate until the error is less than the tolerance, the function value is zero or the maximum number of iterations is reached
        while previous_error > tolerance and f_x != 0 and counter < iterations:
            # Sets the previous x value and calculate the new value of x using the Newton-Raphson method
            x_previous = x
            x = x - f_x / derivative.subs(variable, x).evalf(precision)

            # Calculate the function value at the new x value
            f_x = function.subs(variable, x).evalf(precision)

            # Store the values in the lists
            values_list.append(str(x))
            function_values_list.append(str(f_x))

            # Calculate the error and increment the counter
            if absolute_error:
                error = abs(x - x_previous)
            else:
                error = abs((x - x_previous) / x)
            counter += 1

            # Store the error in the list, update the previous error and add the counter to the list
            error_values_list.append(str(error))
            previous_error = error
            counter_values_list.append(counter)

        # Return the list of iterations, values, function values and errors
        return [counter_values_list, values_list, function_values_list, error_values_list]
    

def secant(function: sp.Expr, variable: sp.Symbol, initial: float, second_initial: float, tolerance: float = 0.5, iterations: int = 100, absolute_error: bool = True, precision: int = 16) -> Tuple[List[int], List[str], List[str], List[str]]:
    """
    Find the root of a function using the secant method.
    
    Args:
        function: The function for which to find the root.
        initial: Initial value of the independent variable.
        second_initial: Second initial value of the independent variable.
        tolerance: Tolerance for the root (default 0.5).
        iterations: Maximum number of iterations to perform (default 100).
        absolute_error: If True, the error is calculated as the absolute value of the difference between the current and previous values. If False, the error is calculated as the absolute value of the difference between the current and previous values divided by the current value (default True).
        precision: Number of decimal places to round the values (default 15).
    Returns:
        List or table with the iterations, the values of x, the values of f(x) and the errors.
    """
    # Initialize the lists to store the function values and errors
    function_values_list = []
    values_list = []
    error_values_list = []
    counter_values_list = []
    counter = 0

    # Calculate the function values at the initial points
    f_initial = function.subs(variable, initial).evalf(precision)
    f_second_initial = function.subs(variable, second_initial).evalf(precision)

    # Check if the initial or second initial points are roots
    if f_initial == 0:
        return [[0], [str(initial)], [str(f_initial)], ["0"]]
    elif f_second_initial == 0:
        return [[0], [str(second_initial)], [str(f_second_initial)], ["0"]]
    else:
        # Set the variables needed for the iterations
        x = second_initial
        x_previous = initial
        f_x = f_second_initial
        f_x_previous = f_initial
        # Initialize the error
        previous_error = 1

        # Add the initial previous values to the lists
        values_list.append(str(x_previous))
        function_values_list.append(str(f_x_previous))
        error_values_list.append(str(previous_error))
        counter_values_list.append(counter)

        # Add the initial values to the lists
        values_list.append(str(x))
        function_values_list.append(str(f_x))
        error_values_list.append(str(previous_error))
        counter_values_list.append(counter)

        # Iterate until the error is less than the tolerance, the function value is zero or the maximum number of iterations is reached
        while previous_error > tolerance and f_x != 0 and counter < iterations:
            # Calculate the new value of x using the secant method
            x_new = x - f_x * (x - x_previous) / (f_x - f_x_previous)

            # Set the previous x value and the current x value
            x_previous = x
            x = x_new

            # Calculate the function value at the new x value
            f_x_new = function.subs(variable, x_new).evalf(precision)

            # Set the previous function value and the current function value
            f_x_previous = f_x
            f_x = f_x_new

            # Store the values in the lists
            values_list.append(str(x))
            function_values_list.append(str(f_x))

            # Calculate the error and increment the counter
            if absolute_error:
                error = abs(x - x_previous)
            else:
                error = abs((x - x_previous) / x)
            counter += 1

            # Store the error in the list, update the previous error and add the counter to the list
            error_values_list.append(str(error))
            previous_error = error
            counter_values_list.append(counter)

        # Return the list of iterations, values, function values and errors
        return [counter_values_list, values_list, function_values_list, error_values_list]
