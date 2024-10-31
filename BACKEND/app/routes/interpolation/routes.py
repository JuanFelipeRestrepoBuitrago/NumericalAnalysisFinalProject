from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
import sympy as sp

# Configuration, models, methods and authentication modules imports
from app.config.limiter import limiter
from app.models.models import ResponseError, InterpolationRequest, InterpolationResponse, SplineRequest, SplineResponse, SplineFunction
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception
from app.routes.routes import logger

# Module imports
from app.domain.vander import Vandermonde
from app.domain.newton import Newton
from app.domain.lagrange import Lagrange
from app.domain.spline import Spline


router = APIRouter()


@router.post('/vandermonde/',
                tags=["Interpolation", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Gauss Elimination method",
                response_model=InterpolationResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def vandermonde(request: Request, data: InterpolationRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Find a interpolating polynomial using the Vandermonde method.

    :param request: Request object.
    :param data: InterpolationRequest object.
    :param auth: Authentication token.
    :return: InterpolationResponse object.
    """
    try:
        x = data.x
        y = data.y

        vandermonde = Vandermonde(x, y, precision=data.precision)
        coefficients = vandermonde.solve()

        polynomial = vandermonde.convert_coefficients_to_polynomial(coefficients)
        coefficients = vandermonde.convert_1_n_matrix_to_array(coefficients)
        return InterpolationResponse(polynomial=polynomial, coefficients=coefficients)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/newton/',
                tags=["Interpolation", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Newton's Divided Difference method",
                response_model=InterpolationResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def newton(request: Request, data: InterpolationRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Find a interpolating polynomial using the Newton's Divided Difference method.

    :param request: Request object.
    :param data: InterpolationRequest object.
    :param auth: Authentication token.
    :return: InterpolationResponse object.
    """
    try:
        x = data.x
        y = data.y

        newton = Newton(x, y, precision=data.precision)
        polynomial, coefficients = newton.get_polynomial()

        return InterpolationResponse(polynomial=polynomial, coefficients=coefficients)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/lagrange/',
                tags=["Interpolation", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Lagrange method",
                response_model=InterpolationResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def lagrange(request: Request, data: InterpolationRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Find a interpolating polynomial using the Lagrange method.

    :param request: Request object.
    :param data: InterpolationRequest object.
    :param auth: Authentication token.
    :return: InterpolationResponse object.
    """
    try:
        x = data.x
        y = data.y

        lagrange = Lagrange(x, y, precision=data.precision)
        polynomial, coefficients = lagrange.solve()

        return InterpolationResponse(polynomial=polynomial, coefficients=coefficients)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)
        
        
@router.post('/spline/',
                tags=["Interpolation", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Spline method",
                response_model=SplineResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def spline(request: Request, data: SplineRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Find a interpolating polynomial using the Spline method.

    :param request: Request object.
    :param data: SplineRequest object.
    :param auth: Authentication token.
    :return: SplineResponse object.
    """
    try:
        x = data.x
        y = data.y

        spline = Spline(x, y, precision=data.precision)
        result_array, result_coefficient_array = spline.solve(data.degree)
        functions = [SplineFunction(function=func[0], interval=func[1]) for func in result_array]

        return SplineResponse(functions=functions, coefficients=result_coefficient_array)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)
