from app.utils.utils import raise_exception
from app.routes.routes import logger
import sympy as sp
from typing import List, Tuple
from app.domain.interpolation import Interpolation

class Newton(Interpolation):
    def __init__(self, x: List[float], y: List[float], precision: int = 16):
        self.precision = precision
        super().__init__(x, y)
        self.n = len(x)
        self.difference_table = self.create_difference_table()

    def create_difference_table(self, y_values: sp.Matrix = None, x_values: sp.Matrix = None, n: int = None) -> sp.Matrix:
        """
        Create the difference table for the given y values.

        :param y_values: The y values to create the difference table.
        :param x_values: The x values to create the difference table.
        :param n: The number of points to interpolate.

        :return: The difference table.
        """
        if y_values is None:
            y_values = self.y

        if x_values is None:
            x_values = self.x

        if n is None:
            n = self.n

        # Initialize the difference table
        difference_table = sp.zeros(n, n + 1)
        difference_table[:, 0] = x_values
        difference_table[:, 1] = y_values

        # Calculate divided differences
        for j in range(2, n + 1):
            for i in range(j - 1, n):
                if difference_table[i, 0] - difference_table[i - j + 1, 0] == 0:
                    raise_exception(f'No se puede dividir por 0, el elemento {i} de la columna 0 y el elemento {i - j + 1} de la columna 0 son iguales en la tabla de diferencias divididas', logger=logger)
                # Calculate the divided difference
                difference_table[i, j] = ((difference_table[i, j - 1] - difference_table[i - 1, j - 1]) / (difference_table[i, 0] - difference_table[i - j + 1, 0])).evalf(self.precision)

        return difference_table
    
    def extract_coefficients(self, difference_table: sp.Matrix = None, n: int = None) -> sp.Matrix:
        """
        Extract the coefficients from the difference table.

        :param difference_table: The difference table to extract the coefficients.
        :param n: The number of points to interpolate.

        :return: The coefficients as a (n, 1) matrix.
        """
        if difference_table is None:
            difference_table = self.difference_table

        if n is None:
            n = self.n
        
        # Initialize the coefficients as a (n, 1) matrix
        coefficients = sp.zeros(n, 1)

        # Extract the coefficients
        for i in range(n):
            coefficients[i] = difference_table[i, i + 1]

        return coefficients
    
    def get_polynomial(self, x: sp.Matrix = None, coefficients: sp.Matrix = None, n: int = None) -> Tuple[str, List[str]]:
        """
        Get the polynomial from the coefficients.

        :param x: The x values to interpolate.
        :param coefficients: The coefficients of the polynomial.
        :param n: The number of points to interpolate.

        :return: The polynomial as an expression and a list with the coefficients as strings.
        """
        if x is None:
            x = self.x

        if coefficients is None:
            coefficients = self.extract_coefficients()

        if n is None:
            n = self.n

        x_symbol = sp.symbols('x')

        # Initialize the polynomial
        polynomial = coefficients[0]
        accumulator = 1

        # Calculate the polynomial
        for i in range(1, n):
            accumulator *= (x_symbol - x[i - 1])
            polynomial += (coefficients[i] * accumulator).evalf(self.precision)

        polynomial = sp.simplify(polynomial)

        polynomial_coefficients = sp.Poly(polynomial, x_symbol).all_coeffs()
        polynomial_coefficients = [str(coefficient) for coefficient in polynomial_coefficients]
        return self.expression_to_string(polynomial), polynomial_coefficients
    