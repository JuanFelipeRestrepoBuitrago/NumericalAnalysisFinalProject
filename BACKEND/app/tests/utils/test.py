from app.utils.utils import parse_expression
from app.routes.routes import logger
from fastapi.exceptions import HTTPException


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
    expression = "x**2 + 2*x + 1 + xlog(x)"
    try:
        expr, variables = parse_expression(expression, logger)
        raise AssertionError("The expression is invalid and should raise an exception")
    except HTTPException as e:
        assert e.detail == "Expresión Inválida, verifique la guía de expresiones"

    # Test the function with an invalid expression
    expression = "x**2 + 2*x + 1 + x(x)"
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