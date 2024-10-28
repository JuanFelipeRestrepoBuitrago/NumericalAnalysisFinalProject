from typing import List
from app.utils.utils import raise_exception
import sympy as sp
from app.routes.routes import logger

class Interpolation:
    def __init__(self, x: List[float], y: List[float]):
        self.x = self.transform_array_to_1_column_matrix(x)
        self.y = self.transform_array_to_1_column_matrix(y)

        # Verify that the number of elements in x is equal to the number of elements in y
        if len(x) != len(y):
            raise_exception('El número de elementos en x debe ser igual al número de elementos en y para realizar la interpolación', logger=logger)

        # Verify that the x values are unique
        if len(x) != len(set(x)):
            raise_exception('Los valores de x deben ser únicos para realizar la interpolación, no se permiten valores repetidos', logger=logger)

    def transform_array_to_1_column_matrix(self, array: List[float]) -> sp.Matrix:
        """
        Transform an array to a 1 column matrix

        :param array: Array to transform
        """
        return sp.Matrix(array).reshape(len(array), 1)

    def convert_polynomial_to_string(self, coefficients: sp.Matrix) -> str:
        """
        Convert the coefficients of the polynomial to a string

        :param coefficients: Sympy Matrix with the coefficients of the polynomial
        """
        x = sp.symbols('x')

        # Create the polynomial
        polynomial = 0
        for i, coefficient in enumerate(coefficients):
            polynomial += coefficient * x ** i

        return str(polynomial)
