from app.utils.utils import raise_exception
from app.routes.routes import logger
import numpy as np


def regressive_substitution(Ab: np.array, n: int):
    """
    This function performs the regressive substitution method to solve a system of equations.
    :param Ab: numpy array with the coefficients of the system of equations
    :param n: length of the system of equations
    :param logger: logger object
    :return: numpy array with the solution of the system of equations
    """
    # Create an array to store the solution
    x = np.zeros(n)

    # Find the solution for the last equation
    x[n - 1] = Ab[n - 1, n] / Ab[n - 1, n - 1]

    # Find the solution for the rest of the equations
    for i in range(n - 2, -1, -1):
        # Calculate the sum of the products of the coefficients and the solutions
        sum = 0
        for p in range(i + 1, n):
            # Add the product of the coefficient and the respective solution
            sum += Ab[i, p] * x[p]
            
        # Calculate the solution for the current equation, x_i = (b_i - sum) / a_ii
        x[i] = (Ab[i, n] - sum) / Ab[i, i]
    # Return the solution
    return x


def partial_pivot(Ab: np.array, n: int, k: int):
    """
    This function performs the partial pivot method to solve a system of equations.
    :param Ab: numpy array with the coefficients of the system of equations
    :param n: length of the system of equations
    :param k: current iteration
    :param logger: logger object
    :return: numpy array with the coefficients of the system of equations after the partial pivot method
    """
    # Find the maximum value in the current column
    max = np.abs(Ab[k, k])
    max_row = k

    # Iterate over the rows to find the maximum value
    for s in range(k + 1, n):
        # Check if the current value is greater than the maximum value
        if np.abs(Ab[s, k]) > max:
            max = np.abs(Ab[s, k])
            max_row = s

    # Check if the maximum value is zero
    if max == 0:
        raise_exception(SystemError("El sistema no tiene solución única"), logger)

    # Swap the rows if the maximum value is not in the current row
    if max_row != k:
        # Swap the rows
        Ab[[k, max_row]] = Ab[[max_row, k]]

    # Return the coefficients of the system of equations after the partial pivot method
    return Ab
