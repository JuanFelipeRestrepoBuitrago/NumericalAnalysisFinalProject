from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

# Configuration, models, methods and authentication modules imports
from app.config.limiter import limiter
from app.models.models import ResponseError, NumericalMethodResponse, BisectionModel
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception, parse_expression
from app.utils.methods import bisection as bisection_method
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
def bisection(request: Request, data: BisectionModel, auth: dict = Depends(auth_handler.authenticate)):
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

        iterations, x, fx, error = bisection_method(function, variable, data.a, data.b, tolerance=data.tolerance, iterations=data.max_iterations, absolute_error=absolute_error)

        return NumericalMethodResponse(Iterations=iterations, Xn=x, Fx=fx, Error=error)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)