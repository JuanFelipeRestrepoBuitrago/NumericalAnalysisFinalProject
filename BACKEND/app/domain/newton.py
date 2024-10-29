import sympy as sp
from app.utils.utils import raise_exception
from app.routes.routes import logger
from typing import List, Tuple
from app.domain.interpolation import Interpolation

class Newton(Interpolation):
    def __init__(self, x: List[float], y: List[float], precision: int = 16):
        self.precision = precision
        super().__init__(x, y)
        self.n = len(x)
        self.difference_table = self.create_difference_table()

    def create_difference_table(self, y_values: sp.Matrix = None, x_values: sp.Matrix = None) -> sp.Matrix:
        """
        Create the difference table for the given y values.

        :param y_values: The y values to create the difference table.
        :param x_values: The x values to create the difference table.

        :return: The difference table.
        """
        if y_values is None:
            y_values = self.y

        if x_values is None:
            x_values = self.x

        # Initialize the difference table
        difference_table = sp.zeros(self.n, self.n + 1)
        difference_table[:, 0] = x_values
        difference_table[:, 1] = y_values

        # Calculate divided differences
        for j in range(2, self.n + 1):
            for i in range(j - 1, self.n):
                # Calculate the divided difference
                difference_table[i, j] = ((difference_table[i, j - 1] - difference_table[i - 1, j - 1]) / (difference_table[i, 0] - difference_table[i - j + 1, 0])).evalf(self.precision)

        return difference_table