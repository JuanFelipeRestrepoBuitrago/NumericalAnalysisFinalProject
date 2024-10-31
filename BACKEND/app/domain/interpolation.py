from typing import List
from app.utils.utils import raise_exception
import sympy as sp
from app.routes.routes import logger
import re

class Interpolation:
    def __init__(self, x: List[float], y: List[float]):
        if len(x) == 0 or len(y) == 0:
            raise_exception("Las 'x' y 'y' no pueden estar vacíos", logger=logger)
        elif len(x) != len(y):
            raise_exception('El número de elementos en x debe ser igual al número de elementos en y para realizar la interpolación', logger=logger)
        elif len(x) != len(set(x)):
            raise_exception('Los valores de x deben ser únicos para realizar la interpolación, no se permiten valores repetidos', logger=logger)
        elif len(x) < 2 or len(y) < 2:
            raise_exception('Se necesitan al menos 2 puntos para realizar la interpolación', logger=logger)
            
        # Convert x and y elements to floats
        x = [float(element) for element in x]
        y = [float(element) for element in y]

        # Sort the x and y values
        x, y = zip(*sorted(zip(x, y)))
        
        self.x = self.transform_array_to_1_column_matrix(x)
        self.y = self.transform_array_to_1_column_matrix(y)



    def transform_array_to_1_column_matrix(self, array: List[float]) -> sp.Matrix:
        """
        Transform an array to a 1 column matrix

        :param array: Array to transform
        """
        return sp.Matrix(array).reshape(len(array), 1)

    def convert_coefficients_to_polynomial(self, coefficients: sp.Matrix) -> str:
        """
        Convert the coefficients of the polynomial to a string

        :param coefficients: Sympy Matrix with the coefficients of the polynomial
        """
        x = sp.symbols('x')

        # Create the polynomial
        polynomial = 0
        for i, coefficient in enumerate(coefficients):
            polynomial += coefficient * x ** (len(coefficients) - i - 1)

        return self.expression_to_string(polynomial)
    
    def convert_1_n_matrix_to_array(self, matrix: sp.Matrix) -> List[str]:
        """
        Convert a 1 column or 1 row matrix to an array

        :param matrix: Matrix to convert of 1 column and n rows
        """
        if matrix.shape[0] != 1 and matrix.shape[1] != 1:
            raise_exception('La matriz debe ser de 1 columna o 1 fila', logger=logger)
        
        return [str(element) for element in matrix]
    
    def expression_to_string(self, expression: sp.Expr) -> str:
        """
        Convert a sympy expression to a string

        :param expression: Sympy expression to convert
        """
        x = sp.symbols('x')
        
        # Get the polynomial as a Poly object to access coefficients
        poly = sp.Poly(expression, x)

        # Extract coefficients in descending order
        coefficients = poly.all_coeffs()

        # Construct the polynomial as a string in descending order of powers
        polynomial_str = " + ".join([f"{coeff}*x**{i}" for i, coeff in enumerate(reversed(coefficients))][::-1])
        
        # Remove terms like "0.0*x**n"
        polynomial_str = re.sub(r'(\s\+\s)?\-?(?<!\d)0(\.0+)?\*x\*\*\d+', '', polynomial_str)

        # Clean up any redundant terms like "0*x**n" and handle signs
        polynomial_str = polynomial_str.replace("+ -", "- ").replace("*x**0", "").replace(" 1*x", " x").replace("x**1", "x")

        # Return the polynomial as a string
        return polynomial_str
    
    def float_matrix_to_string_array(self, matrix: sp.Matrix) -> List[List[str]]:
        """
        Convert a float matrix to a string array

        :param matrix: Matrix to convert
        """
        matrix = matrix.tolist()
        
        # Convert the matrix to a string matrix
        for i in range(len(matrix)):
            if type(matrix[i]) != list:
                matrix[i] = str(matrix[i])
            else:
                for j in range(len(matrix[i])):
                    matrix[i][j] = str(matrix[i][j])
                
        return matrix
