from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

# Configuration, models, methods and authentication modules imports
from app.config.limiter import limiter
from app.models.models import ResponseError, NumericalMethodResponse, BisectionFalseRuleModel, FixedPointModel, NewtonRaphsonModel, SecantModel, FirstNewtonModified, SecondNewtonModified
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception, parse_expression
from app.domain.methods import bisection as bisection_method, false_rule as false_rule_method, fixed_point as fixed_point_method, newton_raphson as newton_raphson_method, secant as secant_method, first_modified_newton_method as first_modified_newton_method, second_modified_newton_method as second_modified_newton_method
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
@limiter.limit("15/minute")
def bisection(request: Request, data: BisectionFalseRuleModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    Bisection method route.

    This route is used to calculate the roots of a mathematical expression using the Bisection method.

    Args:
        request (Request): The request object.
        data (BisectionFalseRuleModel): The Bisection model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")

        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error, message = bisection_method(function, variable, data.initial, data.final, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        logger.info(f"Request successful: {message}")

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error, Message=message)
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
@limiter.limit("15/minute")
def false_rule(request: Request, data: BisectionFalseRuleModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    False Rule method route.

    This route is used to calculate the roots of a mathematical expression using the False Rule method.

    Args:
        request (Request): The request object.
        data (BisectionFalseRuleModel): The False Rule model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")

        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error, message = false_rule_method(function, variable, data.initial, data.final, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        logger.info(f"Request successful: {message}")

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error, Message=message)
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
@limiter.limit("15/minute")
def fixed_point(request: Request, data: FixedPointModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    Fixed Point method route.

    This route is used to calculate the roots of a mathematical expression using the Fixed Point method.

    Args:
        request (Request): The request object.
        data (FixedPointModel): The Fixed Point model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")

        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        function_g = parse_expression(data.g_expression, logger, variable_character=variable.name)[0]

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error, message = fixed_point_method(function, variable, function_g, data.initial, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        logger.info(f"Request successful: {message}")

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error, Message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/newton_raphson/',
                tags=["Numerical Methods", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Newton Raphson method",
                response_model=NumericalMethodResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def newton_raphson(request: Request, data: NewtonRaphsonModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    Newton Raphson method route.

    This route is used to calculate the roots of a mathematical expression using the Newton Raphson method.

    Args:
        request (Request): The request object.
        data (NewtonRaphsonModel): The Newton Raphson model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")

        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        if data.derivative_expression is not None:
            derivative = parse_expression(data.derivative_expression, logger, variable_character=variable.name)[0]
        else:
            derivative = None

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error, message = newton_raphson_method(function, variable, data.initial, derivative=derivative, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        logger.info(f"Request successful: {message}")

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error, Message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/secant/',
                tags=["Numerical Methods", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Secant method",
                response_model=NumericalMethodResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def secant(request: Request, data: SecantModel, auth: dict = Depends(auth_handler.authenticate)):
    """
    Secant method route.

    This route is used to calculate the roots of a mathematical expression using the Secant method.

    Args:
        request (Request): The request object.
        data (SecantModel): The Secant model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")

        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        absolute_error = True if data.error_type == "absolute" else False

        iterations, x, fx, error, message = secant_method(function, variable, data.initial, data.second_initial, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision)

        logger.info(f"Request successful: {message}")

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error, Message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)

@router.post('/first_modified_newton_method/',
                tags=["Numerical Methods", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="First Modified Newton method",
                response_model=NumericalMethodResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def first_modified_newton(request: Request, data: FirstNewtonModified, auth: dict = Depends(auth_handler.authenticate)):
    """
    First Modified Newton method route.

    This route is used to calculate the roots of a mathematical expression using the First Modified Newton method.

    Args:
        request (Request): The request object.
        data (FirstNewtonModified): The First Modified Newton model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")

        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        absolute_error = True if data.error_type == "absolute" else False

        if data.derivative_expression is not None:
            derivative = parse_expression(data.derivative_expression, logger, variable_character=variable.name)[0]
        else:
            derivative = None

        iterations, x, fx, error, message = first_modified_newton_method(function, variable, data.initial, multiplicity=data.multiplicity, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision, derivative=derivative)

        logger.info(f"Request successful: {message}")

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error, Message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger) 


@router.post('/second_modified_newton_method/',
                tags=["Numerical Methods", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Second Modified Newton method",
                response_model=NumericalMethodResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def second_modified_newton(request: Request, data: SecondNewtonModified, auth: dict = Depends(auth_handler.authenticate)):
    """
    Second Modified Newton method route.

    This route is used to calculate the roots of a mathematical expression using the Second Modified Newton method.

    Args:
        request (Request): The request object.
        data (SecondNewtonModified): The Second Modified Newton model.
        auth (dict): The authentication dictionary.

    Returns:
        NumericalMethodResponse: The response model. Table with iterations, xn, f(xn) and error.

    Raises:
        HTTPException: If an error occurs during the method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        function, variables = parse_expression(data.expression, logger)
        variable = variables[0]

        absolute_error = True if data.error_type == "absolute" else False

        if data.derivative_expression is not None:
            derivative = parse_expression(data.derivative_expression, logger, variable_character=variable.name)[0]
        else:
            derivative = None

        if data.second_derivative_expression is not None:
            second_derivative = parse_expression(data.second_derivative_expression, logger, variable_character=variable.name)[0]
        else:
            second_derivative = None

        iterations, x, fx, error, message = second_modified_newton_method(function, variable, data.initial, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error, precision=data.precision, derivative=derivative, second_derivative=second_derivative)

        logger.info(f"Request successful: {message}")

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error, Message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)
