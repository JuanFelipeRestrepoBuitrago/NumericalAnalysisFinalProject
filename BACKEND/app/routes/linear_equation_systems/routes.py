from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
import numpy as np
import sympy as sp

# Configuration, models, methods and authentication modules imports
from app.config.limiter import limiter
from app.models.models import ResponseError, GaussEliminationRequest, GaussEliminationResponse, LUFactorizationRequest, LUFactorizationResponse, IterativeMatrixEquationSystemRequest, IterativeMatrixEquationSystemResponse, SorRequest, SpectralAndConvergenceResponse
from app.domain.jacobi import Jacobi
from app.domain.gauss_seidel import GaussSeidel
from app.domain.sor import Sor
from app.domain.gaussian_elimination import GaussianElimination
from app.domain.lu_factorization import LUFactorization
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception, calculate_spectral_radius
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
@limiter.limit("15/minute")
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
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
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
        absolute_error = gauss_elimination_object.get_set_absolute_error(order=data.order)

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


@router.post('/lu_factorization/',
                tags=["Linear Equations System", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="LU Factorization method",
                response_model=LUFactorizationResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def lu_factorization(request: Request, data: LUFactorizationRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    LU Factorization method.
    
    This endpoint solves a system of linear equations using the LU Factorization method.
    
    Arguments:
    data: LUFactorizationRequest: JSON with the matrix of coefficients, the vector of solutions, and the number of equations.
    
    Returns:
    LUFactorizationResponse: JSON with the solutions of the system of equations, the vectorial errors, and the absolute error.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        # Get the data from the request
        A = np.array(data.A)
        b = np.array(data.b)
        n = data.n
        pivot_type = data.pivot_type

        # Create the object to solve the system of equations
        lu_factorization_object = LUFactorization(A, b, n, precision=data.precision)

        # Solve the system of equations
        x, L, U = lu_factorization_object.solve(pivot_type=pivot_type)
        vectorial_error = lu_factorization_object.get_set_vectorial_error()
        absolute_error = lu_factorization_object.get_set_absolute_error(order=data.order)

        # Convert to Strings
        x = lu_factorization_object.convert_matrix_to_string(x)
        L = lu_factorization_object.convert_matrix_to_string(L)
        U = lu_factorization_object.convert_matrix_to_string(U)
        vectorial_error = lu_factorization_object.convert_matrix_to_string(vectorial_error)
        absolute_error = str(absolute_error)

        return LUFactorizationResponse(x=x, L=L, U=U, vectorial_error=vectorial_error, absolute_error=absolute_error)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/jacobi/',
                tags=["Linear Equations System", "Matrix and Iterative", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Jacobi method",
                response_model=IterativeMatrixEquationSystemResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def jacobi(request: Request, data: IterativeMatrixEquationSystemRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Jacobi method.
    
    This endpoint solves a system of linear equations using the Jacobi method.
    
    Arguments:
    data: IterativeMatrixEquationSystemRequest: JSON with the matrix of coefficients, the vector of solutions, the initial guess, and the precision.
    
    Returns:
    IterativeMatrixEquationSystemResponse: JSON with the solutions of the system of equations, the vectorial errors, and the absolute error.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        # Get the data from the request
        A = np.array(data.A)
        b = np.array(data.b)
        x_initial = np.array(data.x_initial)

        # Create the object to solve the system of equations
        jacobi_object = Jacobi(A, b, x_initial, precision=data.precision)

        # Create the absolute_error boolean
        error = True if data.error_type == "absolute" else False

        # Solve the system of equations
        if data.method_type == "iterative":
            result = jacobi_object.iterative_solve(tol=data.tol, max_iter=data.max_iter, order=data.order, absolute_error=error)
        else:
            result = jacobi_object.matrix_solve(tol=data.tol, max_iter=data.max_iter, order=data.order, absolute_error=error)
        iterations = result[0]
        x = result[1]
        error = result[2]
        message = result[3]

        return IterativeMatrixEquationSystemResponse(iterations=iterations, x=x, error=error, message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/jacobi/spectral_radius_and_convergence/',
                tags=["Linear Equations System", "Matrix and Iterative", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Jacobi method",
                response_model=SpectralAndConvergenceResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def jacobi_spectral_radius_and_convergence(request: Request, data: IterativeMatrixEquationSystemRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Get the spectral radius and the convergence of the Jacobi method.
    
    This endpoint calculates the spectral radius and the convergence of the Jacobi method.
    
    Arguments:
    data: IterativeMatrixEquationSystemRequest: JSON with the matrix of coefficients, the vector of solutions, the initial guess, and the precision.
    
    Returns:
    SpectralAndConvergenceResponse: JSON with the spectral radius and the convergence of the Jacobi method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        # Get the data from the request
        A = np.array(data.A)
        b = np.array(data.b)
        x_initial = np.array(data.x_initial)

        # Create the object to solve the system of equations
        jacobi_object = Jacobi(A, b, x_initial, precision=data.precision)

        # Calculate the spectral radius and the convergence
        spectral_radius = jacobi_object.get_t_spectral_radius()
        convergence = jacobi_object.converges()

        return SpectralAndConvergenceResponse(spectral_radius=spectral_radius, convergence=convergence)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)
    

@router.post('/gauss_seidel/',
                tags=["Linear Equations System", "Matrix and Iterative", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Gauss Seidel method",
                response_model=IterativeMatrixEquationSystemResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def gauss_seidel(request: Request, data: IterativeMatrixEquationSystemRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Gauss Seidel method.
    
    This endpoint solves a system of linear equations using the Gauss Seidel method.
    
    Arguments:
    data: IterativeMatrixEquationSystemRequest: JSON with the matrix of coefficients, the vector of solutions, the initial guess, and the precision.
    
    Returns:
    IterativeMatrixEquationSystemResponse: JSON with the solutions of the system of equations, the vectorial errors, and the absolute error.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        # Get the data from the request
        A = sp.Matrix(data.A)
        b = sp.Matrix(data.b)
        x_initial = sp.Matrix(data.x_initial)

        # Create the object to solve the system of equations
        gauss_seidel_object = GaussSeidel(A, b, x_initial, precision=data.precision)

        # Create the absolute_error boolean
        error = True if data.error_type == "absolute" else False

        # Solve the system of equations
        if data.method_type == "iterative":
            result = gauss_seidel_object.iterative_solve(tol=data.tol, max_iter=data.max_iter, order=data.order, absolute_error=error)
        else:
            result = gauss_seidel_object.matrix_solve(tol=data.tol, max_iter=data.max_iter, order=data.order, absolute_error=error)
        iterations = result[0]
        x = result[1]
        error = result[2]
        message = result[3]

        return IterativeMatrixEquationSystemResponse(iterations=iterations, x=x, error=error, message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/gauss_seidel/spectral_radius_and_convergence/',
                tags=["Linear Equations System", "Matrix and Iterative", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="Gauss Seidel method",
                response_model=SpectralAndConvergenceResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def gauss_seidel_spectral_radius_and_convergence(request: Request, data: IterativeMatrixEquationSystemRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Get the spectral radius and the convergence of the Gauss Seidel method.
    
    This endpoint calculates the spectral radius and the convergence of the Gauss Seidel method.
    
    Arguments:
    data: IterativeMatrixEquationSystemRequest: JSON with the matrix of coefficients, the vector of solutions, the initial guess, and the precision.
    
    Returns:
    SpectralAndConvergenceResponse: JSON with the spectral radius and the convergence of the Gauss Seidel method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        # Get the data from the request
        A = sp.Matrix(data.A)
        b = sp.Matrix(data.b)
        x_initial = sp.Matrix(data.x_initial)

        # Create the object to solve the system of equations
        gauss_seidel_object = GaussSeidel(A, b, x_initial, precision=data.precision)

        # Calculate the spectral radius and the convergence
        spectral_radius = gauss_seidel_object.get_t_spectral_radius()
        convergence = gauss_seidel_object.converges()

        return SpectralAndConvergenceResponse(spectral_radius=spectral_radius, convergence=convergence)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/sor/',
                tags=["Linear Equations System", "Matrix and Iterative", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="SOR method",
                response_model=IterativeMatrixEquationSystemResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def sor(request: Request, data: SorRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    SOR method.
    
    This endpoint solves a system of linear equations using the SOR method.
    
    Arguments:
    data: IterativeMatrixEquationSystemRequest: JSON with the matrix of coefficients, the vector of solutions, the initial guess, the relaxation factor, and the precision.
    
    Returns:
    IterativeMatrixEquationSystemResponse: JSON with the solutions of the system of equations, the vectorial errors, and the absolute error.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        # Get the data from the request
        A = sp.Matrix(data.A)
        b = sp.Matrix(data.b)
        x_initial = sp.Matrix(data.x_initial)

        # Create the object to solve the system of equations
        sor_object = Sor(A, b, x_initial, precision=data.precision)

        # Create the absolute_error boolean
        error = True if data.error_type == "absolute" else False

        # Solve the system of equations
        if data.method_type == "iterative":
            result = sor_object.iterative_solve(w=data.omega, tol=data.tol, max_iter=data.max_iter, order=data.order, absolute_error=error)
        else:
            result = sor_object.matrix_solve(w=data.omega, tol=data.tol, max_iter=data.max_iter, order=data.order, absolute_error=error)
        iterations = result[0]
        x = result[1]
        error = result[2]
        message = result[3]

        return IterativeMatrixEquationSystemResponse(iterations=iterations, x=x, error=error, message=message)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)


@router.post('/sor/spectral_radius_and_convergence/',
                tags=["Linear Equations System", "Matrix and Iterative", "Protected"],
                status_code=status.HTTP_200_OK,
                summary="SOR method",
                response_model=SpectralAndConvergenceResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("15/minute")
def sor_spectral_radius_and_convergence(request: Request, data: SorRequest, auth: dict = Depends(auth_handler.authenticate)):
    """
    Get the spectral radius and the convergence of the SOR method.
    
    This endpoint calculates the spectral radius and the convergence of the SOR method.
    
    Arguments:
    data: IterativeMatrixEquationSystemRequest: JSON with the matrix of coefficients, the vector of solutions, the initial guess, the relaxation factor, and the precision.
    
    Returns:
    SpectralAndConvergenceResponse: JSON with the spectral radius and the convergence of the SOR method.
    """
    try:
        logger.info(f"Request from {request.client.host} to {request.url.path}: {data}")
        
        # Get the data from the request
        A = sp.Matrix(data.A)
        b = sp.Matrix(data.b)
        x_initial = sp.Matrix(data.x_initial)
        w = data.omega

        # Create the object to solve the system of equations
        sor_object = Sor(A, b, x_initial, precision=data.precision)

        # Calculate the spectral radius and the convergence
        spectral_radius = sor_object.get_t_spectral_radius(w=data.omega)
        convergence = sor_object.converges(w=data.omega)

        return SpectralAndConvergenceResponse(spectral_radius=spectral_radius, convergence=convergence)
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise_exception(e, logger)
