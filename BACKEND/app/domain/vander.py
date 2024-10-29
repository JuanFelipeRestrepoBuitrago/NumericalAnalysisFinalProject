import sympy as sp
from app.utils.utils import raise_exception
from app.routes.routes import logger
from typing import List, Tuple
from app.domain.interpolation import Interpolation

class Vandermonde(Interpolation):
    def __init__(self, x: List[float], y: List[float], precision: int = 16):
        self.precision = precision
        super().__init__(x, y)
        self.n = len(x)
        self.vandermonde_matrix = self.create_vandermonde_matrix()

    def create_vandermonde_matrix(self, x_values: sp.Matrix = None) -> sp.Matrix:
        """
        Create the Vandermonde matrix for the given x values.

        :param x_values: The x values to create the Vandermonde matrix.

        :return: The Vandermonde matrix.
        """
        if x_values is None:
            x_values = self.x

        return sp.Matrix([[x**i for i in range(self.n - 1, - 1, -1)] for x in x_values])

    def solve(self, vandermonde_matrix: sp.Matrix = None, y_values: sp.Matrix = None) -> sp.Matrix:
        """
        Solve the interpolation problem using the Vandermonde matrix.

        :param vandermonde_matrix: The Vandermonde matrix.
        :param y_values: The y values.

        :return: The coefficients of the polynomial.
        """
        if vandermonde_matrix is None:
            vandermonde_matrix = self.vandermonde_matrix

        if y_values is None:
            y_values = self.y

        # Fix the typo here to apply precision correctly
        return (vandermonde_matrix.inv() * y_values).evalf(self.precision)
