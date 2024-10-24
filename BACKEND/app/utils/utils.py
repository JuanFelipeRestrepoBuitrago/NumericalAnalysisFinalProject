from logging import Logger
from fastapi import HTTPException, status
import sympy as sp
from typing import Tuple
from sympy.core.sympify import SympifyError
import re
import numpy as np


def raise_exception(e: Exception, logger: Logger):
    """
    Raise an HTTPException and log the error

    Arguments:
        e (Exception) : The exception that was raised
        logger (Logger) : The logger instance to log

    Raises:
        HTTPException : The HTTPException with the error message
    """
    logger.error(f"Error : {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )


def parse_expression(expression: str, logger: Logger, variable_character: str = None) -> Tuple[sp.Expr, list[sp.Symbol]]:
    """
    Parse the expression and return the sympy expression and the variables in the expression

    Arguments:
        expression (str) : The expression to parse
        logger (Logger) : The logger instance to log
        variable_character (str) : The character to use as the variable

    Returns:
        tuple : The sympy expression and the variables in the expression
    """
    # Check if the expression is empty to raise an exception
    if not expression:
        raise_exception(ValueError("La expresión o función no puede ser vacía"), logger)

    # Try to parse the expression, if it fails raise an exception
    try:
        expr = sp.sympify(expression)
    except (TypeError, SyntaxError, SympifyError) as e:
        raise_exception(SyntaxError("Expresión Inválida, verifique la guía de expresiones"), logger)

    # Check if the expression is a function and get the variables
    if variable_character is None:
        variables = list(expr.free_symbols)
    else:
        variables = [sp.symbols(variable_character)]

    # Check if the expression doesn't contains variables to raise an exception
    if not variables:
        raise_exception(ValueError("La expresión o función no contiene variables"), logger)

    # Check if there are any variables next to another variable or expression, example: xx, xln(x)
    for variable in variables:
        if re.search(rf"{variable.name}\(", expression) or re.search(rf"\){variable.name}", expression) or len(variable.name) > 1:
            raise_exception(SyntaxError("Expresión Inválida, verifique la guía de expresiones"), logger)
        
    # Return the expression and the variables
    return expr, variables
    

def construct_augmented_matrix(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Constructs the augmented matrix Ab from A and b.

    Args:
        A (numpy.ndarray): The coefficient matrix of size (n, n).
        b (numpy.ndarray): The constant vector of size (n, 1) or (n,).

    Returns:
        numpy.ndarray: The augmented matrix [A | b].
    """
    # Reshape b to ensure it's a column vector (n x 1)
    if b.ndim == 1:
        b = b.reshape(-1, 1)
    
    # Horizontally stack A and b to create the augmented matrix
    if b.shape == (A.shape[0], 1):
        Ab = np.hstack((A, b))
    elif b.shape == (1, A.shape[0]):
        Ab = np.hstack((A, b.T))
    
    return Ab


def calculate_spectral_radius(A: sp.Matrix, precision: int = 16) -> str:
    """
    Calculate the spectral radius of the matrix A

    Arguments:
        A (sp.Matrix) : The matrix to calculate the spectral radius
        precision (int) : The precision to calculate the spectral radius

    Returns:
        str : The spectral radius of the matrix A
    """
    # Get the eigenvalues of the matrix A
    eigenvalues = A.eigenvals()

    # Get the maximum eigenvalue
    max_eigenvalue = str(max([sp.Abs(eig.evalf(precision)).evalf(precision) for eig in eigenvalues.keys()]))

    return max_eigenvalue


def is_strictly_diagonally_dominant(A: np.ndarray) -> bool:
    """
    Check if the matrix A is strictly diagonally dominant

    Arguments:
        A (np.ndarray) : The matrix to check

    Returns:
        bool : True if the matrix is strictly diagonally dominant, False otherwise
    """
    # Get the diagonal elements of the matrix A
    diagonal = np.abs(A.diagonal())
    
    # Get the sum of the absolute values of the elements of each row without the diagonal element
    row_sum = np.sum(np.abs(A), axis=1) - diagonal
    
    # Check if the matrix is strictly diagonally dominant
    return np.all(diagonal > row_sum)
