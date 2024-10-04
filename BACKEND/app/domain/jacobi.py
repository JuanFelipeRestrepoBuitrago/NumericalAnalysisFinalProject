from app.utils.utils import raise_exception
from app.routes.routes import logger
from decimal import Decimal, getcontext
import numpy as np
from typing import List, Tuple


class Jacobi:
    def __init__(self, A: np.array, b: np.array, x_initial:np.array, n: int = None, precision: int = 16):
        getcontext().prec = precision
        self.A = A.astype(float)
        self.b = b.astype(float)    
        self.x_initial = x_initial.astype(float)

        try:
            self.validate_input(A, b, n, x_initial)
        except IndexError:
            raise_exception(IndexError("Las matrices deben ser definidas con 2 paréntesis, el principal y dentro de este las filas separadas por comas. Ejemplo: [[1, 2], [3, 4]]"), logger)

        self.A = self.redefine_to_decimal(A)
        self.b = self.redefine_to_decimal(b)
        self.x_initial = self.redefine_to_decimal(x_initial)

        if n is None:
            self.n = self.A.shape[0]
        else:
            self.n = n

        # Construct the augmented matrix
        self.Ab = None
        self.x = None

        # Vectorial and Scalar error to None
        self.vectorial_error = None
        self.scalar_error = None

    def redefine_to_decimal(self, matrix: np.array):
        """
        This function redefines the values of a numpy array to Decimal.

        :param matrix: numpy array to redefine
        :return: numpy array with the values redefined to Decimal
        """
        new_matrix = np.array(matrix, dtype=object)
        # Iterate over the rows
        for i in range(matrix.shape[0]):
            # Iterate over the columns
            for j in range(matrix.shape[1]):
                # Redefine the value to Decimal
                new_matrix[i, j] = Decimal(str(matrix[i, j]))

        # Return the numpy array with the values redefined to Decimal
        return new_matrix
        
    def validate_input(self, A: np.array, b: np.array, n: int, x_initial: np.array):
        """
        This function validates the input for the Gaussian Elimination method.

        :param A: numpy array with the coefficients of the system of equations
        :param b: numpy array with the solutions of the system of equations
        :param n: length of the system of equations
        :param x_initial: numpy array with the initial guess for the solution
        """
        # Check if the matrix A is square
        if A.shape[0] != A.shape[1]:
            raise_exception(ValueError("La matriz A no es cuadrada"), logger)

        # Check if the b vector is correct
        if A.shape[0] != b.shape[0] and A.shape[0] != b.shape[1]:
            raise_exception(ValueError("La longitud del vector b no es igual al número de filas de la matriz A"), logger)
        elif b.shape[0] != 1 and b.shape[1] != 1:
            raise_exception(ValueError("b debe ser un vector columna, no una matriz"), logger)

        # Check if the initial guess vector is correct
        if x_initial is not None and A.shape[0] != x_initial.shape[0] and A.shape[0] != x_initial.shape[1]:
            raise_exception(ValueError("La longitud del vector x inicial no es igual al número de filas de la matriz A"), logger)
        elif x_initial is not None and x_initial.shape[0] != 1 and x_initial.shape[1] != 1:
            raise_exception(ValueError("x inicial debe ser un vector columna, no una matriz"), logger)

        # Check if the length of n is equal to the number of rows in the matrix A
        if n is not None and n != A.shape[0]:
            raise_exception(ValueError("La longitud de n no es igual al número de filas y columnas de la matriz A"), logger)

    def iterative_solve(self, tol: float, max_iter: int = 100, A: np.array = None, b: np.array = None, x_initial: np.array = None, absolute_error: bool = True, order: int = 0) -> Tuple[List[int], List[List[str]], List[str]]:
        """
        This function solves a system of linear equations using the Jacobi method.

        :param A: numpy array with the coefficients of the system of equations
        :param b: numpy array with the solutions of the system of equations
        :param x_initial: numpy array with the initial guess for the solution
        :param tol: tolerance for the solution
        :param max_iter: maximum number of iterations
        :param absolute_error: boolean to determine if the absolute or relative error is calculated
        :param order: Order of the vectorial norm, 0 for infinite
        :return: List with the number of iterations, the solutions for each iteration and the absolute or relative error for each iteration
        """
        if A is None:
            A = self.A.copy()
        if b is None:
            b = self.b.copy()
        if x_initial is None:
            x_initial = self.x_initial.copy()

        if order == 0:
            order = np.inf
        elif order < 0:
            raise_exception(ValueError("El orden de la norma no es válido, este debe ser 0 o entero positivo"), logger)

        # Initialize the lists to store the function values and errors
        values_list = None
        error_values_list = []
        counter_values_list = []
        counter = 0
        error = tol + 1

        # Initialize the current x vector
        x_current = x_initial.copy()

        # Fill the table with the initial values
        counter_values_list.append(counter)
    
        if x_current.shape[0] == 1:  # Shape (1, n)
            values_list = [[str(val[0, 0])] for val in np.split(x_current, x_current.shape[1], axis=1)]
        elif x_current.shape[1] == 1:  # Shape (n, 1)
            values_list = [[str(val[0, 0])] for val in np.split(x_current, x_current.shape[0], axis=0)]

        error_values_list.append("-")

        # Iterate while the error is greater than the tolerance and the number of iterations is less than the maximum
        while error > tol and counter < max_iter:
            # Create the new x vector
            x_new = x_current.copy()

            # Iterate over the rows of the matrix A
            for i in range(A.shape[0]):
                # Initialize the sum of the elements of the row
                sum_row = 0

                # Iterate over the columns of the matrix A
                for j in range(A.shape[1]):
                    # Check if the element is not in the diagonal
                    if i != j:
                        # Sum the element of the row
                        if x_current.shape[0] == 1:
                            sum_row += A[i, j] * x_current[0, j]
                        elif x_current.shape[1] == 1:
                            sum_row += A[i, j] * x_current[j, 0]

                if b.shape[0] == 1:
                    b_element = b[0, i]
                else:
                    b_element = b[i, 0]

                # Calculate the new value of the x vector
                if x_new.shape[0] == 1:
                    x_new[0, i] = (b_element - sum_row) / A[i, i]
                elif x_new.shape[1] == 1:
                    x_new[i, 0] = (b_element - sum_row) / A[i, i]

            # Calculate the error
            if absolute_error:
                if x_current.shape[0] == 1:
                    error = np.linalg.norm(x_new.T - x_current.T, ord=order)
                elif x_current.shape[1] == 1:
                    error = np.linalg.norm(x_new - x_current, ord=order)
            else:
                if x_current.shape[0] == 1:
                    error = np.linalg.norm(x_new.T - x_current.T / x_new.T, ord=order)
                elif x_current.shape[1] == 1:
                    error = np.linalg.norm(x_new - x_current / x_new, ord=order)

            # Update the current x vector
            x_current = x_new

            # Append the values to the lists
            counter += 1
            counter_values_list.append(counter)
            if x_current.shape[0] == 1:  # Shape (1, n)
                splitted = np.split(x_current, x_current.shape[1], axis=1)
            elif x_current.shape[1] == 1:  # Shape (n, 1)
                splitted = np.split(x_current, x_current.shape[0], axis=0)

            [values_list[i].append(str(splitted[i][0][0])) for i in range(len(values_list))]

            error_values_list.append(str(error))

        # Store the values of the solution and the errors
        self.x = x_current
        self.vectorial_error = error
        self.scalar_error = error

        return counter_values_list, values_list, error_values_list





        
