from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
import numpy as np

# Configuration, models, methods and authentication modules imports
from app.config.limiter import limiter
from app.models.models import ResponseError, GaussEliminationRequest, GaussEliminationResponse
from app.domain.gaussian_elimination import GaussianElimination
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception, parse_expression
from app.routes.routes import logger


router = APIRouter()


@router.post('/gauss_elimination/',
                tags=["Linear Equations System", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Gauss Elimination method",
                response_model=GaussEliminationResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("5/minute")
def gauss_elimination(request: Request, data: GaussEliminationRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Gauss Elimination method.
    
    This endpoint solves a system of linear equations using the Gauss Elimination method.
    
    Arguments:
    data: GaussEliminationRequest: JSON with the matrix of coefficients, the vector of solutions, and the number of equations.
    
    Returns:
    GaussEliminationResponse: JSON with the solutions of the system of equations, the vectorial errors, and the absolute error.
    """
    try:
        logger.info(f"Request from {request.client.host}: {data}")
        
        # Get the data from the request
        A = np.array(data.A)
        b = np.array(data.b)
        n = data.n
        pivot_type = data.pivot_type

        # Create the object to solve the system of equations
        gauss_elimination_object = GaussianElimination(A, b, n, precision=data.precision)

        # Solve the system of equations
        x = gauss_elimination_object.solve(pivot_type=pivot_type)
        vectorial_error = gauss_elimination_object.get_set_vectorial_error()
        absolute_error = gauss_elimination_object.get_set_absolute_error()

        # Convert to Strings
        x = gauss_elimination_object.convert_matrix_to_string(x)
        vectorial_error = gauss_elimination_object.convert_matrix_to_string(vectorial_error)
        absolute_error = str(absolute_error)

        return GaussEliminationResponse(x=x, vectorial_error=vectorial_error, absolute_error=absolute_error)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)
