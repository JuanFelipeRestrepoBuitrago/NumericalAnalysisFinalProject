from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

# Configuration, models, methods and authentication modules imports
from app.config.limiter import limiter
from app.models.models import ResponseError, NumericalMethodResponse, BisectionFalseRuleModel, FixedPointModel
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception, parse_expression
from app.utils.methods import bisection as bisection_method, false_rule as false_rule_method, fixed_point as fixed_point_method
from app.routes.routes import logger

router = APIRouter()

@router.post('/bisection/',
                tags=["Numerical Methods", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Bisection method",
                response_model=NumericalMethodResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("5/minute")
def bisection(request: Request, data: BisectionFalseRuleModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    Bisection method route.

    This route is used to calculate the roots of a mathematical expression using the Bisection method.

    Args:
        request (Request): The request object.
        data (Bisection): The Bisection model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error = bisection_method(function, variable, data.initial, data.final, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/false_rule/',
                tags=["Numerical Methods", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="False Rule method",
                response_model=NumericalMethodResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("5/minute")
def false_rule(request: Request, data: BisectionFalseRuleModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    False Rule method route.

    This route is used to calculate the roots of a mathematical expression using the False Rule method.

    Args:
        request (Request): The request object.
        data (Bisection): The Bisection model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error = false_rule_method(function, variable, data.initial, data.final, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)

@router.post('/fixed_point/',
                tags=["Numerical Methods", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Fixed Point method",
                response_model=NumericalMethodResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                }) 
@limiter.limit("5/minute")
def fixed_point(request: Request, data: FixedPointModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    Fixed Point method route.

    This route is used to calculate the roots of a mathematical expression using the Fixed Point method.

    Args:
        request (Request): The request object.
        data (Bisection): The Bisection model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        function_g = parse_expression(data.g_expression, logger, variable_character=variable.name)

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error = fixed_point_method(function, variable, function_g, data.initial, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)
