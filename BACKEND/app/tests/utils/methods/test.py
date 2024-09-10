from app.utils.methods import bisection, false_rule
from app.utils.utils import parse_expression
from app.routes.routes import logger
from fastapi.exceptions import HTTPException
from decimal import Decimal


def test_bisection():
    # Test 1
    function, variables = parse_expression("x**2 - 4", logger)
    variable = variables[0]
    initial = 0
    final = 3
    tolerance = 0.5e-10
    iterations = 10
    absolute_error = True
    result = bisection(function, variable, initial, final, tolerance, iterations, absolute_error)

    assert result[1][0] == 1.5
    assert result[1][1] == 2.25
    assert result[2][0] == -1.75
    assert result[2][1] == 1.0625
    assert result[3][1] == 0.75

    # Test 2
    function, variables = parse_expression("x**2 - 4", logger)
    variable = variables[0]
    initial = 0
    final = 3
    tolerance = 0.5e-10
    iterations = 10
    absolute_error = False
    result = bisection(function, variable, initial, final, tolerance, iterations, absolute_error)

    assert result[1][0] == 1.5
    assert result[1][1] == 2.25
    assert result[2][0] == -1.75
    assert result[2][1] == 1.0625
    assert result[3][1] == 0.333333333333333333

    # Test 3
    function, variables = parse_expression("x**2 - 4", logger)
    variable = variables[0]
    initial = -10
    final = -4
    tolerance = 0.5e-10
    iterations = 10
    absolute_error = False
    try:
        result = bisection(function, variable, initial, final, tolerance, iterations, absolute_error)
    except HTTPException as e:
        assert e.detail == "La función no tiene cambio de signo en el intervalo dado"


def test_false_rule():
    # Test 1
    function, variables = parse_expression("exp(x) + 3 * cos(x)", logger)
    variable = variables[0]
    initial = -2
    final = -1.5
    tolerance = 0.5e-100
    iterations = 5
    absolute_error = True
    result = false_rule(function, variable, initial, final, tolerance, iterations, absolute_error)

    assert result[1][0] == -1.6405736739860801
    assert result[1][1] == -1.6358029581446338
    assert result[2][0] == -0.01529342132032005
    assert result[2][1] == -8.667300290643443e-5
    assert result[3][1] == 0.0047707158414462825

    # Test 2
    function, variables = parse_expression("exp(x) + 3 * cos(x)", logger)
    variable = variables[0]
    initial = -2
    final = -1.5
    tolerance = 0.5e-100
    iterations = 5
    absolute_error = False
    result = false_rule(function, variable, initial, final, tolerance, iterations, absolute_error)

    assert result[1][0] == -1.6405736739860801
    assert result[1][1] == -1.6358029581446338
    assert result[2][0] == -0.01529342132032005
    assert result[2][1] == -8.667300290643443e-5
    assert result[3][1] == 0.0029164367368899615

    # Test 3
    function, variables = parse_expression("exp(x) + 3 * cos(x)", logger)
    variable = variables[0]
    initial = -1
    final = -6
    tolerance = 0.5e-100
    iterations = 5
    absolute_error = False
    try:
        result = false_rule(function, variable, initial, final, tolerance, iterations, absolute_error)
    except HTTPException as e:
        assert e.detail == "La función no tiene cambio de signo en el intervalo dado"
