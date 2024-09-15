from app.utils.utils import raise_exception, construct_augmented_matrix
from app.routes.routes import logger
import numpy as np


class GaussianElimination:
    def __init__(self, A: np.array, b: np.array, n: int = None):
        self.A = A
        self.b = b

        try:
            self.validate_input(A, b, n)
        except IndexError:
            raise_exception(IndexError("Las matrices deben ser definidas con 2 paréntesis, el principal y dentro de este las filas separadas por comas. Ejemplo: [[1, 2], [3, 4]]"), logger)

        if n is None:
            self.n = A.shape[0]
        else:
            self.n = n

        # Construct the augmented matrix
        self.Ab = construct_augmented_matrix(A, b)
        self.x = None
        
    def validate_input(self, A: np.array, b: np.array, n: int):
        """
        This function validates the input for the Gaussian Elimination method.
        :param A: numpy array with the coefficients of the system of equations
        :param b: numpy array with the solutions of the system of equations
        :param n: length of the system of equations
        """
        # Check if the matrix A is square
        if A.shape[0] != A.shape[1]:
            raise_exception(ValueError("La matriz A no es cuadrada"), logger)

        # Check if the b vector is correct
        if A.shape[0] != b.shape[0] and A.shape[0] != b.shape[1]:
            raise_exception(ValueError("La longitud del vector b no es igual al número de filas de la matriz A"), logger)
        elif b.shape[0] != 1 and b.shape[1] != 1:
            raise_exception(ValueError("b debe ser un vector columna, no una matriz"), logger)

        # Check if the length of n is equal to the number of rows in the matrix A
        if n is not None and n != A.shape[0]:
            raise_exception(ValueError("La longitud de n no es igual al número de filas y columnas de la matriz A"), logger)

    def regressive_substitution(self, Ab: np.array = None, n: int = None):
        """
        This function performs the regressive substitution method to solve a system of equations.
        :param Ab: numpy array with the coefficients of the system of equations
        :param n: length of the system of equations
        """
        if Ab is None:
            Ab = self.Ab
        if n is None:
            n = self.n

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

        # Store the solution in the object
        self.x = x
        # Return the solution
        return x

    def pivot(self, k: int, pivot_type: int, mark: np.array = None, Ab: np.array = None, n: int = None):
        """
        This function performs the total pivot method to solve a system of equations.

        :param k: current iteration
        :param pivot_type: number 1 or 2 to indicate if the pivot is partial or total
        :param mark: numpy array with the permutation of the columns in order to keep track of the solutions
        :param Ab: numpy array with the coefficients of the system of equations
        :param n: length of the system of equations
        :return: numpy array with the coefficients of the system of equations after the total pivot method
        """
        if Ab is None:
            Ab = self.Ab
        if n is None:
            n = self.n

        # Create an array to store the permutation of the columns
        if mark is None:
            mark = np.arange(n)

        # Initialize necessary variables
        max = 0
        max_col = k
        max_row = k
        
        # Check if the pivot is total
        if pivot_type == 2:
            column_condition = n
        else:
            column_condition = k + 1
        # Iterate over the rows
        for i in range(k, n):
            # Iterate over the columns to find the maximum value
            for j in range(k, column_condition):
                # Check if the current value is greater than the maximum value
                if np.abs(Ab[i, j]) > max:
                    max = np.abs(Ab[i, j])
                    max_row = i
                    max_col = j

        # Check if the maximum value is zero
        if max == 0:
            raise_exception(SystemError("El sistema no tiene solución única"), logger)

        # Swap the columns if the maximum value is not in the current column
        if max_col != k:
            # Swap the columns
            Ab[:, [k, max_col]] = Ab[:, [max_col, k]]
            
            # Swap the elements in the permutation array
            mark[k], mark[max_col] = mark[max_col], mark[k]

        # Swap the rows if the maximum value is not in the current row
        if max_row != k:
            # Swap the rows
            Ab[[k, max_row]] = Ab[[max_row, k]]

        # Return the coefficients of the system of equations after the total pivot method
        return Ab, mark
