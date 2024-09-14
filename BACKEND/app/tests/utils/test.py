from app.utils.utils import parse_expression, construct_augmented_matrix
from app.routes.routes import logger
from fastapi.exceptions import HTTPException
import numpy as np


def test_parse_expression():
    """
    Test the parse_expression function from the utils module
    """
    # Test the function with a valid expression
    expression = "x**2 + 2*x + 1"
    expr, variables = parse_expression(expression, logger)
    assert str(expr) == expression
    assert len(variables) == 1
    assert str(variables[0]) == "x"

    # Test the function with a valid expression
    expression = "(x**2 + 2*x)*log(x) + 1"
    expr, variables = parse_expression(expression, logger)
    assert str(expr) == expression
    assert len(variables) == 1
    assert str(variables[0]) == "x"
    
    # Test the function with a valid expression and a custom variable character
    expression = "a**2 + 2*a + 1"
    expr, variables = parse_expression(expression, logger)
    assert str(expr) == expression
    assert len(variables) == 1
    assert str(variables[0]) == "a"
    
    # Test the function with an empty expression
    expression = ""
    try:
        expr, variables = parse_expression(expression, logger)
    except HTTPException as e:
        assert e.detail == "La expresión o función no puede ser vacía"
    
    # Test the function with an invalid expression
    expression = "x**2 + 2*x + 1 +"
    try:
        expr, variables = parse_expression(expression, logger)
    except HTTPException as e:
        assert e.detail == "Expresión Inválida, verifique la guía de expresiones"

    # Test the function with an invalid expression
    expression = "x**2 + 2*x + 1 + 3x"
    try:
        expr, variables = parse_expression(expression, logger)
    except HTTPException as e:
        assert e.detail == "Expresión Inválida, verifique la guía de expresiones"

    # Test the function with an invalid expression
    expression = "x**2 + 2*x + 1 + x(x)"
    try:
        expr, variables = parse_expression(expression, logger)
        raise AssertionError("The expression is invalid and should raise an exception")
    except HTTPException as e:
        assert e.detail == "Expresión Inválida, verifique la guía de expresiones"

    # Test the function with an invalid expression
    expression = "x**2 + 2*x + 1 + xx"
    try:
        expr, variables = parse_expression(expression, logger)
        raise AssertionError("The expression is invalid and should raise an exception")
    except HTTPException as e:
        assert e.detail == "Expresión Inválida, verifique la guía de expresiones"

    # Test the function with an invalid expression
    expression = "xx"
    try:
        expr, variables = parse_expression(expression, logger)
        raise AssertionError("The expression is invalid and should raise an exception")
    except HTTPException as e:
        assert e.detail == "Expresión Inválida, verifique la guía de expresiones"
    
    # Test the function with an expression without variables
    expression = "1 + 2 + 3"
    try:
        expr, variables = parse_expression(expression, logger)
    except HTTPException as e:
        assert e.detail == "La expresión o función no contiene variables"

def test_construct_augmented_matrix():
    # Test 1
    A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = np.array([10, 11, 12])
    Ab = np.array([[1, 2, 3, 10], [4, 5, 6, 11], [7, 8, 9, 12]])
    assert np.array_equal(construct_augmented_matrix(A, b), Ab), "Test failed for a 3x3 matrix"

    # Test 2
    A = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    b = np.array([13, 14, 15])
    Ab = np.array([[1, 2, 3, 4, 13], [5, 6, 7, 8, 14], [9, 10, 11, 12, 15]])
    assert np.array_equal(construct_augmented_matrix(A, b), Ab), "Test failed for a 3x4 matrix"

    # Test 3
    A = np.array([[1, 2], [3, 4]])
    b = np.array([[5], [6]])
    Ab = np.array([[1, 2, 5], [3, 4, 6]])
    assert np.array_equal(construct_augmented_matrix(A, b), Ab), "Test failed for a 2x2 matrix"
