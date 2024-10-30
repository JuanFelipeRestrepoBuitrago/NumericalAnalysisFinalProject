import sympy as sp
from typing import List, Tuple
from app.domain.interpolation import Interpolation

class Spline(Interpolation):
    def __init__(self, x: List[float], y: List[float], precision: int = 16):
        self.precision = precision
        super().__init__(x, y)
        self.n = len(x)

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
            A[i, c] = self.x[i]
            A[i, c + 1] = 1
            b[i] = self.y[i]
            c += 2

        c = 0
        for i in range(1, n):
            A[i + n - 2, c] = self.x[i]
            A[i + n - 2, c + 1] = 1
            b[i + n - 2] = self.y[i]
            c += 2

        # Solve the system
        solution = (A.inv() * b).evalf(self.precision)

        # Reshape the solution
        solution = solution.reshape(n - 1, 2)
        return solution

    def solve_cubic_spline(self) -> List[List[float]]:
        """
        Calculate the cubic spline coefficients for a given set of points (x, y).
        :return: A list of coefficients for each segment.
        """
        n = self.n
        A = sp.zeros(4 * (n - 1), 4 * (n - 1))
        b = sp.zeros(4 * (n - 1), 1)
        
        # Filling the A matrix and b vector for cubic spline
        c = 0
        for i in range(n - 1):
            A[i, c] = self.x[i]**3
            A[i, c + 1] = self.x[i]**2
            A[i, c + 2] = self.x[i]
            A[i, c + 3] = 1
            b[i] = self.y[i]
            c += 4

        c = 0
        for i in range(1, n):
            A[i + n - 2, c] = self.x[i]**3
            A[i + n - 2, c + 1] = self.x[i]**2
            A[i + n - 2, c + 2] = self.x[i]
            A[i + n - 2, c + 3] = 1
            b[i + n - 2] = self.y[i]
            c += 4

        c = 0
        for i in range(1, n - 1):
            A[2 * (n - 1) + i - 1, c] = 3 * self.x[i]**2
            A[2 * (n - 1) + i - 1, c + 1] = 2 * self.x[i]
            A[2 * (n - 1) + i - 1, c + 2] = 1
            A[2 * (n - 1) + i - 1, c + 4] = -3 * self.x[i]**2
            A[2 * (n - 1) + i - 1, c + 5] = -2 * self.x[i]
            A[2 * (n - 1) + i - 1, c + 6] = -1
            c += 4

        c = 0
        for i in range(1, n - 1):
            A[3 * (n - 1) - 1 + i, c] = 6 * self.x[i]
            A[3 * (n - 1) - 1 + i, c + 1] = 2
            A[3 * (n - 1) - 1 + i, c + 4] = -6 * self.x[i]
            A[3 * (n - 1) - 1 + i, c + 5] = -2
            c += 4

        # Boundary conditions for the cubic spline
        A[-2, 0] = 6 * self.x[0]
        A[-2, 1] = 2
        A[-1, -4] = 6 * self.x[-1]
        A[-1, -3] = 2

        # Solve the system
        solution = (A.inv() * b).evalf(self.precision)
        return solution
