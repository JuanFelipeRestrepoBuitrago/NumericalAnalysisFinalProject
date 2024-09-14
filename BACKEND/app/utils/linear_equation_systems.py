from app.utils.utils import raise_exception
from app.routes.routes import logger
import numpy as np


def regressive_substitution(Ab: np.array, n: int, logger=logger):
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