import sympy as sp
from app.utils.utils import raise_exception
from app.routes.routes import logger
from typing import List, Tuple
from app.domain.interpolation import Interpolation

class Vandermonde(Interpolation):
    def __init__(self, x: List[float], y: List[float]) -> None:
        super().__init__(x, y)
        self.n = len(x)
        self.vandermonde_matrix = self.create_vandermonde_matrix()

    def create_vandermonde_matrix(self, x_values: sp.Matrix = None) -> sp.Matrix:
        """
        Create the Vandermonde matrix for the given x values.

        :param x_values: The x values to create the Vandermonde matrix.
        """
        if x_values is None:
            x_values = self.x

        return sp.Matrix([[x**i for i in range(self.n - 1, - 1, -1)] for x in x_values])

    def _solve(self) -> Tuple[sp.Matrix, sp.Matrix]:
        try:
            return self._vander_matrix.inv() * sp.Matrix(self._y), self._vander_matrix
        except Exception as e:
            logger.error(f"Error: {e}")
            raise_exception("Error in Vander method")

    def _interpolation(self) -> None:
        self._coefficients, self._vander_matrix = self._solve()

    def get_interpolation(self) -> Tuple[sp.Matrix, sp.Matrix]:
        self._interpolation()
        return self._coefficients, self._vander_matrix

