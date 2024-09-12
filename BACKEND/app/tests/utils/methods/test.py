from app.utils.methods import bisection, false_rule, fixed_point, newton_raphson
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

    assert result[1][0] == "1.5"
    assert result[1][1] == "2.25"
    assert result[2][0] == "-1.750000000000000"
    assert result[2][1] == "1.062500000000000"
    assert result[3][1] == "0.75"

    # Test 2
    function, variables = parse_expression("x**2 - 4", logger)
    variable = variables[0]
    initial = 0
    final = 3
    tolerance = 0.5e-10
    iterations = 10
    absolute_error = False
    result = bisection(function, variable, initial, final, tolerance, iterations, absolute_error)

    assert result[1][0] == "1.5"
    assert result[1][1] == "2.25"
    assert result[2][0] == "-1.750000000000000"
    assert result[2][1] == "1.062500000000000"
    assert result[3][1] == "0.3333333333333333"

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

    assert result[1][0] == "-1.640573673986080"
    assert result[1][1] == "-1.635802958144634"
    assert result[2][0] == "-0.01529342132031998"
    assert result[2][1] == "-8.667300290610483e-5"
    assert result[3][1] == "0.004770715841446366"

    # Test 2
    function, variables = parse_expression("exp(x) + 3 * cos(x)", logger)
    variable = variables[0]
    initial = -2
    final = -1.5
    tolerance = 0.5e-100
    iterations = 5
    absolute_error = False
    result = false_rule(function, variable, initial, final, tolerance, iterations, absolute_error)

    assert result[1][0] == "-1.640573673986080"
    assert result[1][1] == "-1.635802958144634"
    assert result[2][0] == "-0.01529342132031998"
    assert result[2][1] == "-8.667300290610483e-5"
    assert result[3][1] == "0.002916436736890013"

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

def test_fixed_point():
    # Test 1
    function, variables = parse_expression("(exp(x)/x) + 3", logger)
    variable = variables[0]
    function_g = parse_expression("-(exp(x)/3)", logger, variable_character=variable.name)[0]
    initial = -1
    tolerance = 0.5e-10
    iterations = 10
    absolute_error = True
    result = fixed_point(function, variable, function_g, initial, tolerance, iterations, absolute_error)

    assert result[1][0] == "-1"
    assert result[1][1] == "-0.1226264803904808"
    assert result[2][0] == "2.632120558828558"
    assert result[2][1] == "-4.213727502041105"
    assert result[3][1] == "0.8773735196095192"

    # Test 2
    function, variables = parse_expression("(exp(x)/x) + 3", logger)
    variable = variables[0]
    function_g = parse_expression("-(exp(x)/3)", logger, variable_character=variable.name)[0]
    initial = -1
    tolerance = 0.5e-10
    iterations = 10
    absolute_error = False
    result = fixed_point(function, variable, function_g, initial, tolerance, iterations, absolute_error)

    assert result[1][0] == "-1"
    assert result[1][1] == "-0.1226264803904808"
    assert result[2][0] == "2.632120558828558"
    assert result[2][1] == "-4.213727502041105"
    assert result[3][1] == "7.154845485377136"


def test_newton_raphson():
    # Test 1
    function, variables = parse_expression("(exp(x)/x) + 3", logger)
    variable = variables[0]
    initial = -1
    tolerance = 0.5e-10
    iterations = 5
    absolute_error = True
    result = newton_raphson(function, variable, initial, tolerance=tolerance, iterations=iterations, absolute_error=absolute_error, precision=16)

    assert result[0][-1] == 5
    assert result[1][0] == "-1"
    assert result[1][1] == "2.577422742688568"
    assert result[2][0] == "2.632120558828558"
    assert result[2][1] == "8.107105370253216"
    assert result[3][1] == "3.577422742688568"

    # Test 2
    function, variables = parse_expression("(exp(x)/x) + 3", logger)
    variable = variables[0]
    initial = -1
    tolerance = 0.5e-10
    iterations = 5
    absolute_error = False
    result = newton_raphson(function, variable, initial, tolerance=tolerance, iterations=iterations, absolute_error=absolute_error, precision=16)

    assert result[0][-1] == 5
    assert result[1][0] == "-1"
    assert result[1][1] == "2.577422742688568"
    assert result[2][0] == "2.632120558828558"
    assert result[2][1] == "8.107105370253216"
    assert result[3][1] == "1.387984471246218"
