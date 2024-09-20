from app.utils.utils import raise_exception, construct_augmented_matrix
from app.routes.routes import logger
from decimal import Decimal, getcontext
import numpy as np
from typing import List


class LUFactorization:
    def __init__(self, A: np.array, b: np.array, n: int = None, precision: int = 16):
        getcontext().prec = precision
        self.A = A.astype(float)
        self.b = b.astype(float)    

        try:
            self.validate_input(A, b, n)
        except IndexError:
            raise_exception(IndexError("Las matrices deben ser definidas con 2 paréntesis, el principal y dentro de este las filas separadas por comas. Ejemplo: [[1, 2], [3, 4]]"), logger)

        self.A = self.redefine_to_decimal(A)
        self.b = self.redefine_to_decimal(b)

        if n is None:
            self.n = self.A.shape[0]
        else:
            self.n = n

        # Construct the augmented matrix
        self.Ab = None
        self.x = None

        # Vectorial and Absolute error to None
        self.vectorial_error = None
        self.absolute_error = None

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

    def progressive_substitution(self, Ab: np.array = None, n: int = None):
        """
        This function performs the progressive substitution method to solve a system of equations.

        :param Ab: numpy array with the coefficients of the system of equations
        :param n: length of the system of equations
        """
        if Ab is None:
            Ab = self.Ab
        if n is None:
            n = self.n

        # Create an array to store the solution
        x = np.array([np.zeros(n)], dtype=object)

        if Ab[0, 0] == 0:
            raise_exception(ValueError("El sistema no tiene solución única"), logger)
        # Find the solution for the first equation
        x[0][0] = Ab[0, n] / Ab[0, 0]

        # Find the solution for the rest of the equations
        for i in range(1, n):
            # Calculate the sum of the products of the coefficients and the solutions
            sum = 0
            for p in range(i):
                # Add the product of the coefficient and the respective solution
                sum += Ab[i, p] * x[0][p]

            # Check if the coefficient is zero
            if Ab[i, i] == 0:
                raise_exception(ValueError("El sistema no tiene solución única"), logger)
            # Calculate the solution for the current equation, x_i = (b_i - sum) / a_ii
            x[0][i] = (Ab[i, n] - sum) / Ab[i, i]

        # Store the solution in the object
        self.x = x
        # Return the solution
        return x

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
        x = np.array([np.zeros(n)], dtype=object)

        if Ab[n - 1, n - 1] == 0:
            raise_exception(ValueError("El sistema no tiene solución única"), logger)
        # Find the solution for the last equation
        x[0][n - 1] = Ab[n - 1, n] / Ab[n - 1, n - 1]

        # Find the solution for the rest of the equations
        for i in range(n - 2, -1, -1):
            # Calculate the sum of the products of the coefficients and the solutions
            sum = 0
            for p in range(i + 1, n):
                # Add the product of the coefficient and the respective solution
                sum += Ab[i, p] * x[0][p]
                
            # Check if the coefficient is zero
            if Ab[i, i] == 0:
                raise_exception(ValueError("El sistema no tiene solución única"), logger)
            # Calculate the solution for the current equation, x_i = (b_i - sum) / a_ii
            x[0][i] = (Ab[i, n] - sum) / Ab[i, i]

        # Store the solution in the object
        self.x = x
        # Return the solution
        return x

    def pivot(self, k: int, pivot_type: int, permutation_matrix: np.array = None, Ab: np.array = None, n: int = None) -> List[np.array]:
        """
        This function performs the total pivot method to solve a system of equations.

        :param k: current iteration
        :param pivot_type: number 1 or 2 to indicate if the pivot is partial or total
        :param permutation_matrix: numpy matrix with the permutation of the rows
        :param Ab: numpy array with the coefficients of the system of equations
        :param n: length of the system of equations
        :return: numpy array with the coefficients of the system of equations after the total pivot method
        """
        if Ab is None:
            Ab = self.Ab
        if n is None:
            n = self.n

        # Create an array to store the permutation of the rows
        if permutation_matrix is None:
            permutation_matrix = self.redefine_to_decimal(np.eye(n))

        # Initialize necessary variables
        max = Ab[k, k]
        max_row = k
        
        # Check if the pivot is total
        if pivot_type != 1:
            raise_exception(ValueError("El tipo de pivote no es válido"), logger)

        # Iterate over the rows
        for i in range(k + 1, n):
            # Check if the current element is greater than the maximum
            if abs(Ab[i, k]) > abs(max):
                # Update the maximum and the row
                max = Ab[i, k]
                max_row = i

        # Check if the maximum is zero
        if max == 0:
            raise_exception(ValueError("El sistema no tiene solución única"), logger)

        # Check if the maximum is different from the current element
        if max_row != k:
            # Swap the rows in the augmented matrix
            Ab[[k, max_row]] = Ab[[max_row, k]]

            # Swap the rows in the permutation matrix
            permutation_matrix[[k, max_row]] = permutation_matrix[[max_row, k]]

        # Return the augmented matrix and the permutation matrix
        return Ab, permutation_matrix
    
    def organize_solution(self, x: np.array, mark: np.array) -> np.array:
        """
        This function organizes the solution of the system of equations after the total pivot method.

        :param x: numpy array with the solutions of the system of equations
        :param mark: numpy array with the permutation of the columns in order to keep track of the solutions
        :return: numpy array with the organized solutions of the system of equations
        """
        # Create an array to store the organized solution
        organized_x = np.array([[Decimal("0") for _ in range(x.shape[1])]], dtype=object)

        # Organize the solutions
        for i in range(x.shape[1]):

            organized_x[0][mark[i]] = x[0][i]

        self.x = organized_x
        # Return the organized solutions
        return organized_x
    
    def get_set_vectorial_error(self, x: np.array = None, A: np.array = None, b: np.array = None) -> np.array:
        """
        This function calculates the vectorial error of the solution of a system of equations.

        :param x: numpy array with the solutions of the system of equations
        :param A: numpy array with the coefficients of the system of equations
        :param b: numpy array with the solutions of the system of equations
        :return: numpy array with the vectorial error of the solution of the system of equations
        """
        if x is None:
            if self.x is None:
                raise_exception(ValueError("La solución no ha sido calculada"), logger)
            else:
                x = self.x
        if A is None:
            A = self.A
        if b is None:
            b = self.b

        # Calculate the vectorial error
        error = (np.dot(A, x.T) - b.T).T

        # Store the vectorial error
        self.vectorial_error = error        
        
        # Return the vectorial error
        return error
    
    def get_set_absolute_error(self, vectorial_error: np.array = None, order: int = 0) -> Decimal:
        """
        This function calculates the absolute error of the solution of a system of equations.

        :param vectorial_error: numpy array with the vectorial error of the solution of the system of equations
        :return: decimal number with the absolute error of the solution of the system of equations
        """
        if vectorial_error is None:
            if self.vectorial_error is None:
                raise_exception(ValueError("El error vectorial no ha sido calculado"), logger)
            else:
                vectorial_error = self.vectorial_error

        if order == 0:
            # Calculate the absolute error with the infinity norm
            error = np.linalg.norm(vectorial_error, ord=np.inf)
        elif order < 0:
            raise_exception(ValueError("El orden de la norma no es válido, este debe ser 0 o entero positivo"), logger)
        else:
            # Calculate the absolute error with the order
            error = np.linalg.norm(vectorial_error, ord=order)

        # Store the absolute error
        self.absolute_error = error

        # Return the absolute error
        return error
    
    def solve(self, A: np.array = None, b: np.array = None, n: int = None, pivot_type: int = None) -> np.array:
        """
        This function performs the Gaussian Elimination method to solve a system of equations.

        :param A: numpy array with the coefficients of the system of equations
        :param b: numpy array with the solutions of the system of equations
        :param n: length of the system of equations
        :param pivot_type: number 1 or 2 to indicate if the pivot is partial or total, None for no pivot
        :return: numpy array with the solutions of the system of equations
        """
        if A is None:
            A = self.A
        if b is None:
            b = self.b
        if n is None:
            n = self.n

        # Construct the augmented matrix
        Ab = construct_augmented_matrix(A, b)
        # Build the permutation matrix
        permutation_matrix = np.eye(n)

        # Iterate over the rows
        for k in range(n - 1):
            # Perform the pivot method
            if pivot_type is not None and pivot_type == 1:
                Ab, permutation_matrix = self.pivot(k, pivot_type, permutation_matrix, Ab, n)

            # Iterate over the rows
            for i in range(k + 1, n):
                # Calculate the factor to eliminate the coefficient
                factor = Ab[i, k] / Ab[k, k]

                # Iterate over the columns
                for j in range(k, n + 1):
                    # Update the coefficient
                    Ab[i, j] = Ab[i, j] - factor * Ab[k, j]

        # Perform the regressive substitution method
        x = self.regressive_substitution(Ab=Ab, n=n)

        # Organize the solution
        x = self.organize_solution(x, mark)
        return x
    
    def convert_matrix_to_string(self, matrix: np.array) -> List[List[str]]:
        """
        This function converts a numpy array to a list of lists of strings.
        :param matrix: numpy array to convert
        :return: list of lists of strings
        """
        # Create an array to store the strings
        string_matrix = []

        # Iterate over the rows
        for i in range(matrix.shape[0]):
            # Create an array to store the strings of the row
            string_row = []

            # Iterate over the columns
            for j in range(matrix.shape[1]):
                # Convert the value to a string and append it to the row
                string_row.append(str(matrix[i, j]))

            # Append the row to the matrix
            string_matrix.append(string_row)

        # Return the list of lists of strings
        return string_matrix
