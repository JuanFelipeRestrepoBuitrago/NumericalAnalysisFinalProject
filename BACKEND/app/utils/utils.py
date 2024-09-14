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
    Ab = np.hstack((A, b))
    
    return Ab
