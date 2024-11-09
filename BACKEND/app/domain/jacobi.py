from app.utils.utils import raise_exception, calculate_spectral_radius, is_strictly_diagonally_dominant
from app.routes.routes import logger
from decimal import Decimal, getcontext
import numpy as np
from typing import List, Tuple
import sympy as sp
from sympy import oo as sp_inf




class Jacobi:
    def __init__(self, A: np.array, b: np.array, x_initial:np.array, n: int = None, precision: int = 16):
        getcontext().prec = precision
        self.precision = precision
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

    def get_t_spectral_radius(self, A: sp.Matrix = None) -> str:
        """
        This function calculates the spectral radius of the T matrix obtained from the A matrix.

        :param A: numpy array with the coefficients of the system of equations

        :return: String with the spectral radius of the T matrix
        """
        if A is None:
            A = sp.Matrix(self.A)

        # Calculate the T matrix
        D = sp.diag(*A.diagonal())  # Diagonal matrix from A
        L = - (A.lower_triangular() - D)  # Strict lower triangular (excluding diagonal)
        U = - (A.upper_triangular() - D) # Strict upper triangular (excluding diagonal)
        
        T = (D.inv() * (L + U))

        # Calculate the spectral radius
        spectral_radius = calculate_spectral_radius(T, self.precision)

        return spectral_radius
    
    def converges(self, A: sp.Matrix = None) -> str:
        """
        This function checks if the matrix A converges using the spectral radius of the T matrix.

        :param A: numpy array with the coefficients of the system of equations

        :return: String with the result of the convergence
        """
        if A is None:
            A = sp.Matrix(self.A)

        # Check if the spectral radius of T is less than 1
        spectral_radius = self.get_t_spectral_radius(A)
        spectral_radius_condition = float(spectral_radius) < 1

        # Check if the matrix is strictly diagonally dominant
        diagonally_dominant_condition = is_strictly_diagonally_dominant(A)

        if spectral_radius_condition or diagonally_dominant_condition:
            return "El método converge, el radio espectral de T es menor a 1 y/o la matriz es estrictamente diagonal dominante"
        else:
            return "El método no converge, el radio espectral de T es mayor o igual a 1 y la matriz no es estrictamente diagonal dominante"   

    def element_wise_division(self, A: sp.Matrix, B: sp.Matrix) -> sp.Matrix:
        """
        This function divides two matrices element-wise.

        :param A: First matrix
        :param B: Second matrix
        :return: Matrix with the element-wise division
        """
        return sp.Matrix([[A[i, j] / B[i, j] for j in range(A.shape[1])] for i in range(A.shape[0])])

    def iterative_solve(self, tol: float, max_iter: int = 100, A: np.array = None, b: np.array = None, x_initial: np.array = None, absolute_error: bool = True, order: int = 0) -> Tuple[List[int], List[List[str]], List[str], str]:
        """
        This function solves a system of linear equations using the iterative Jacobi method.

        :param A: numpy array with the coefficients of the system of equations
        :param b: numpy array with the solutions of the system of equations
        :param x_initial: numpy array with the initial guess for the solution
        :param tol: tolerance for the solution
        :param max_iter: maximum number of iterations
        :param absolute_error: boolean to determine if the absolute or relative error is calculated
        :param order: Order of the vectorial norm, 0 for infinite
        :return: List with the number of iterations, the solutions for each iteration, the absolute or relative error for each iteration and a message with the result
        """
        if A is None:
            A = sp.Matrix(self.A)
        if b is None:
            b = sp.Matrix(self.b)
        if x_initial is None:
            x_initial = sp.Matrix(self.x_initial)

        if order == 0:
            order = sp_inf
        elif order < 0:
            raise_exception(ValueError("El orden de la norma no es válido, este debe ser 0 o entero positivo"), logger)

        # Initialize the lists to store the function values and errors
        values_list = None
        error_values_list = []
        counter_values_list = []
        counter = 0
        error = tol + 1

        # Initialize the current x vector
        x_current = sp.Matrix(x_initial)

        # Fill the table with the initial values
        counter_values_list.append(counter)

        if x_current.shape[0] == 1:
            values_list = [[str(x_current[0, i])] for i in range(x_current.shape[1])]
        elif x_current.shape[1] == 1:
            values_list = [[str(x_current[i, 0])] for i in range(x_current.shape[0])]

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
                if A[i, i] == 0 or A[i, i] == 0.0:
                    raise_exception(ValueError("La matriz A tiene un 0 en la diagonal, por lo que no se puede dividir por este valor. Asegúrese que la matriz A sea no singular (det(A) != 0) y este condicionada para el método de Jacobi"), logger)
                if x_new.shape[0] == 1:
                    x_new[0, i] = ((b_element - sum_row) / A[i, i]).evalf(self.precision)
                elif x_new.shape[1] == 1:
                    x_new[i, 0] = ((b_element - sum_row) / A[i, i]).evalf(self.precision)


            # Calculate the error
            if x_new.shape[0] == 1:
                x_new_element = x_new.T
            elif x_new.shape[1] == 1:
                x_new_element = x_new

            if x_current.shape[0] == 1:
                x_element = x_current.T
            elif x_current.shape[1] == 1:
                x_element = x_current

            if absolute_error:
                error = ((x_new_element - x_element)).norm(order).evalf(self.precision)
            else:
                error = self.element_wise_division((x_new_element - x_element), x_new_element).norm(order).evalf(self.precision)

            # Update the current x vector
            x_current = x_new

            # Append the values to the lists
            counter += 1
            counter_values_list.append(counter)
            if x_current.shape[0] == 1:
                splitted = [x_current[0, i] for i in range(x_current.shape[1])]
            elif x_current.shape[1] == 1:
                splitted = [x_current[i, 0] for i in range(x_current.shape[0])]

            [values_list[i].append(str(splitted[i])) for i in range(len(values_list))]

            error_values_list.append(str(error))

        # Store the values of the solution and the errors
        self.x = x_current
        self.vectorial_error = error
        self.scalar_error = error

        if error > tol:
            message = "El método no converge en {} iteraciones".format(max_iter)
        else:
            message = f"{[str(splitted[i]) for i in range(len(values_list))]} es una aproximación de la solución del sistema con una tolerancia de {tol}"

        return counter_values_list, values_list, error_values_list, message
    
    def matrix_solve(self, tol: float, max_iter: int = 100, A: np.array = None, b: np.array = None, x_initial: np.array = None, absolute_error: bool = True, order: int = 0) -> Tuple[List[int], List[List[str]], List[str], str]:
        """
        This function solves a system of linear equations using the matrix Jacobi method.

        :param A: numpy array with the coefficients of the system of equations
        :param b: numpy array with the solutions of the system of equations
        :param x_initial: numpy array with the initial guess for the solution
        :param tol: tolerance for the solution
        :param max_iter: maximum number of iterations
        :param absolute_error: boolean to determine if the absolute or relative error is calculated
        :param order: Order of the vectorial norm, 0 for infinite
        :return: List with the number of iterations, the solutions for each iteration, the absolute or relative error for each iteration and a message with the result
        """
        if A is None:
            A = sp.Matrix(self.A)
        if b is None:
            b = sp.Matrix(self.b)
        if x_initial is None:
            x_initial = sp.Matrix(self.x_initial)

        if order == 0:
            order = sp_inf
        elif order < 0:
            raise_exception(ValueError("El orden de la norma no es válido, este debe ser 0 o entero positivo"), logger)

        # Initialize the lists to store the function values and errors
        values_list = None
        error_values_list = []
        counter_values_list = []
        counter = 0
        error = tol + 1

        # Initialize the current x vector
        x_current = x_initial

        # Fill the table with the initial values
        counter_values_list.append(counter)
    
        if x_current.shape[0] == 1:
            values_list = [[str(x_current[0, i])] for i in range(x_current.shape[1])]
        elif x_current.shape[1] == 1:
            values_list = [[str(x_current[i, 0])] for i in range(x_current.shape[0])]

        error_values_list.append("-")

        # Initialize the D, L and U matrices
        D = sp.diag(*A.diagonal())  # Diagonal matrix from A
        L = - (A.lower_triangular() - D)  # Strict lower triangular (excluding diagonal)
        U = - (A.upper_triangular() - D) # Strict upper triangular (excluding diagonal)

        # Iterate while the error is greater than the tolerance and the number of iterations is less than the maximum
        while error > tol and counter < max_iter:
            if x_current.shape[0] == 1:
                x_element = x_current.T
            elif x_current.shape[1] == 1:
                x_element = x_current

            if b.shape[0] == 1:
                b_element = b.T
            elif b.shape[1] == 1:
                b_element = b

            # Calculate the T and C matrices
            T = (D.inv().evalf(self.precision) * (L + U).evalf(self.precision)).evalf(self.precision)
            C = (D.inv().evalf(self.precision) * b_element).evalf(self.precision)

            # Calculate the new x vector
            x_new = ((T * x_element).evalf(self.precision) + C).evalf(self.precision)

            if x_new.shape[0] == 1:
                x_new_element = x_new.T
            elif x_new.shape[1] == 1:
                x_new_element = x_new

            # Calculate the error
            if absolute_error:
                error = ((x_new_element - x_element).evalf(self.precision)).norm(order).evalf(self.precision)
            else:
                error = self.element_wise_division((x_new_element - x_element).evalf(self.precision), x_new_element).norm(order).evalf(self.precision)

            # Update the current x vector
            x_current = x_new

            # Append the values to the lists
            counter += 1
            counter_values_list.append(counter)
            if x_current.shape[0] == 1:
                splitted = [x_current[0, i] for i in range(x_current.shape[1])]
            elif x_current.shape[1] == 1:
                splitted = [x_current[i, 0] for i in range(x_current.shape[0])]

            [values_list[i].append(str(splitted[i])) for i in range(len(values_list))]
            
            error_values_list.append(str(error))


        # Store the values of the solution and the errors
        self.x = x_current
        self.vectorial_error = error
        self.scalar_error = error

        if error > tol:
            message = "El método no converge en {} iteraciones".format(max_iter)
        else:
            message = f"{[str(splitted[i]) for i in range(len(values_list))]} es una aproximación de la solución del sistema con una tolerancia de {tol}"

        return counter_values_list, values_list, error_values_list, message