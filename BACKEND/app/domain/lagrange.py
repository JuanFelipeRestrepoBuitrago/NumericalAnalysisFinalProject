import sympy as sp
from typing import List, Tuple
from app.domain.interpolation import Interpolation

class Lagrange(Interpolation):
    def __init__(self, x: List[float], y: List[float], precision: int = 16):
        self.precision = precision
        super().__init__(x, y)
        self.n = len(x)

    def solve(self, x: sp.Matrix = None, y: sp.Matrix = None, n: int = None) -> Tuple[str, List[str]]:
        """
        Solve the interpolation problem using the Lagrange method.

        :param x: The x values to interpolate.
        :param y: The y values to interpolate.
        :param n: The number of points to interpolate.

        :return: The coefficients as a (n, 1) matrix.
        """
        if x is None:
            x = self.x

        if y is None:
            y = self.y

        if n is None:
            n = self.n

        # Symbolic variable
        x_symbol = sp.symbols('x')
        polynomial = 0
        lagrange_polynomials = []

        for i in range(n):
            # Initialize the Lagrange basis polynomial L_i(x) and denominator
            Li = 1
            den = 1

            for j in range(n):
                if i != j:
                    # (x - x_j) for the Lagrange basis polynomial
                    Li *= (x_symbol - x[j])
                    # (x_i - x_j) for the denominator
                    den *= (x[i] - x[j])

            # Add the i-th term of the polynomial (y_i * L_i / den)
            polynomial += (y[i] * Li / den).evalf(self.precision)
            lagrange_polynomials.append(self.expression_to_string((Li / den).evalf(self.precision)))

        # Simplify the polynomial
        polynomial = sp.expand(polynomial)

        polynomial_coefficients = sp.Poly(polynomial, x_symbol).all_coeffs()
        polynomial_coefficients = [str(coefficient) for coefficient in polynomial_coefficients]
        return self.expression_to_string(polynomial), polynomial_coefficients, lagrange_polynomials