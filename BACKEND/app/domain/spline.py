import sympy as sp
from app.utils.utils import raise_exception
from app.routes.routes import logger
from typing import List, Tuple
from app.domain.interpolation import Interpolation

class Spline(Interpolation):
    def __init__(self, x: List[float], y: List[float], precision: int = 16):
        self.precision = precision
        super().__init__(x, y)
        self.n = len(x)
        
    def solve(self, d: int) -> Tuple[List[str], List[List[str]]]:
        """
        Solve the interpolation problem using the spline method.
        
        :param d: The degree of the spline.
        :return: A tuple with the list of functions and the list of coefficients.
        """
        if d == 1:
            result = self.solve_linear_spline()
        elif d == 3:
            result = self.solve_cubic_spline()
        else:
            raise_exception('El grado del spline debe ser 1 o 3', logger=logger)
        
        result_array = []
        result_coefficient_array = []
        
        for i in range(result.shape[0]):
            current_row = result.row(i)
            # Add elements to array with each function with the current row of the matrix
            result_array.append(self.convert_coefficients_to_polynomial(current_row))
            result_coefficient_array.append(self.convert_1_n_matrix_to_array(current_row))
        
        return result_array, result_coefficient_array

    def solve_linear_spline(self, x: sp.Matrix = None, y: sp.Matrix = None, n: int = None) -> sp.Matrix:
        """
        Calculate the linear spline expression for a given set of points (x, y) and return the coefficients.

        :param x: The x values to interpolate.
        :param y: The y values to interpolate.
        :param n: The number of points to interpolate.

        :return: Get the coefficients for the linear spline.
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        if n is None:
            n = self.n

        A = sp.zeros(2 * (n - 1), 2 * (n - 1))
        b = sp.zeros(2 * (n - 1), 1)
        
        # Filling the A matrix and b vector for linear spline
        c = 0
        for i in range(n - 1):
            A[i, c] = x[i]
            A[i, c + 1] = 1
            b[i] = y[i]
            c += 2

        c = 0
        for i in range(1, n):
            A[i + n - 2, c] = x[i]
            A[i + n - 2, c + 1] = 1
            b[i + n - 2] = y[i]
            c += 2

        # Solve the system
        solution = (A.inv() * b).evalf(self.precision)

        # Reshape the solution
        solution = solution.reshape(n - 1, 2)
        return solution

    def solve_cubic_spline(self, x: sp.Matrix = None, y: sp.Matrix = None, n: int = None) -> sp.Matrix:
        """
        Calculate the cubic spline expression for a given set of points (x, y) and return the coefficients.
        
        :param x: The x values to interpolate.
        :param y: The y values to interpolate.
        :param n: The number of points to interpolate.
        
        :return: Get the coefficients for the cubic spline.
        """
        if x is None:
            x = self.x
            
        if y is None:
            y = self.y
            
        if n is None:
            n = self.n
            
        A = sp.zeros(4 * (n - 1), 4 * (n - 1))
        b = sp.zeros(4 * (n - 1), 1)
        
        # Filling the A matrix and b vector for cubic spline
        c = 0
        for i in range(n - 1):
            A[i, c] = x[i]**3
            A[i, c + 1] = x[i]**2
            A[i, c + 2] = x[i]
            A[i, c + 3] = 1
            b[i] = y[i]
            c += 4

        c = 0
        for i in range(1, n):
            A[i + n - 2, c] = x[i]**3
            A[i + n - 2, c + 1] = x[i]**2
            A[i + n - 2, c + 2] = x[i]
            A[i + n - 2, c + 3] = 1
            b[i + n - 2] = y[i]
            c += 4

        c = 0
        for i in range(1, n - 1):
            A[2 * (n - 1) + i - 1, c] = 3 * x[i]**2
            A[2 * (n - 1) + i - 1, c + 1] = 2 * x[i]
            A[2 * (n - 1) + i - 1, c + 2] = 1
            A[2 * (n - 1) + i - 1, c + 4] = -3 * x[i]**2
            A[2 * (n - 1) + i - 1, c + 5] = -2 * x[i]
            A[2 * (n - 1) + i - 1, c + 6] = -1
            c += 4

        c = 0
        for i in range(1, n - 1):
            A[3 * (n - 1) - 1 + i, c] = 6 * x[i]
            A[3 * (n - 1) - 1 + i, c + 1] = 2
            A[3 * (n - 1) - 1 + i, c + 4] = -6 * x[i]
            A[3 * (n - 1) - 1 + i, c + 5] = -2
            c += 4

        # Boundary conditions for the cubic spline
        A[-2, 0] = 6 * x[0]
        A[-2, 1] = 2
        A[-1, -4] = 6 * x[-1]
        A[-1, -3] = 2

        # Solve the system
        solution = (A.inv() * b).evalf(self.precision)
        
        # Reshape the solution
        solution = solution.reshape(n - 1, 4)
        return solution
