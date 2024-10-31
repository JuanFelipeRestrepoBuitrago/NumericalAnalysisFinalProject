from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class ResponseError(BaseModel):
    """
    Data model for API error responses.
    
    Whenever the API encounters an error, be it a user-made error, a server error, or any other type of error,
    it will respond with this model. Having a standardized error response format ensures that clients can
    easily understand and handle errors consistently. The `detail` attribute provides a descriptive message 
    about the specific error, aiding in debugging and issue resolution.

    Attributes:
        detail (str): Description of the error.
    """
    detail: str = Field(description="Description of the error.")

class UserLogin(BaseModel):
    """
    Base data model for user creation and update operations.
    
    This model defines the common attributes that are required for both creating and updating a user. 
    The `username` attribute is used to uniquely identify a user, while the `password` attribute is used 
    to authenticate the user. The `email` attribute is used to contact the user and is optional.

    Attributes:
        username (str): Unique identifier for the user.
        password (str): Password for the user.
    """
    username: str = Field(..., description="Unique identifier for the user.")
    password: str = Field(..., description="Password for the user.")


class UserLoginResponse(BaseModel):
    """
    Data model for user login operations.
    
    This model is used for user login responses. It contains the `access_token` attribute, which is a JWT token and the token type.

    Attributes:
        access_token (str): JWT token for user authentication.
        token_type (str): Type of token.
    """
    access_token: str = Field(description="JWT token for user authentication.")
    token_type: str = Field(description="Type of token.")


class NumericalMethodRequest(BaseModel):
    """
    Data model for numerical method requests.
    
    This model is used for numerical method requests. It contains the `expression` attribute, which represents the mathematical expression to be evaluated.

    Attributes:
        expression (str): Mathematical expression to be evaluated.
        error_type (str): Type of error to be used in the method.
        tolerance (float): Tolerance value for the error in the method.
        max_iterations (int): Maximum number of iterations for the method.
        precision (int): Number of decimal places to round the values.
    """
    expression: str = Field(..., description="Mathematical expression or function to be evaluated.")
    error_type: Literal["absolute", "relative"] = Field("absolute", description="Type of error to be used in the method.")
    tolerance: float = Field(..., description="Tolerance value for the error in the method.")
    max_iterations: int = Field(..., description="Maximum number of iterations for the method.")
    precision: int = Field(16, description="Number of decimal places to round the values.")

class NumericalMethodResponse(BaseModel):
    """
    Data model for numerical method responses.
    
    This model is used for numerical method responses.

    Attributes:
        Iterations (List[int]): List of the number of iterations taken to reach the result.
        Xn (List[float]): List of approximations of the root.
        Fx (List[float]): List of function values at each approximation.
        Error (List[float]): List of errors at each approximation.
    """
    Iterations: List[int] = Field(description="List of the number of iterations taken to reach the result.")
    Xn: List[str] = Field(description="List of approximations of the root.")
    Fx: List[str] = Field(description="List of function values at each approximation.")
    Error: List[str] = Field(description="List of errors at each approximation.")
    Message: str = Field(description="Message to be displayed to the user.")


class BisectionFalseRuleModel(NumericalMethodRequest):
    """
    Data model for the Bisection and False Rule methods.
    
    This model extends the `NumericalMethodRequest` model and adds specific attributes for the Bisection and False Rule methods.

    Attributes:
        initial (float): Initial left bound of the interval.
        final (float): Initial right bound of the interval.
    """
    initial: float = Field(..., description="Initial left bound of the interval.")
    final: float = Field(..., description="Initial right bound of the interval.")

class FixedPointModel(NumericalMethodRequest):
    """
    Data model for the Fixed Point method.
    
    This model extends the `NumericalMethodRequest` model and adds specific attributes for the Fixed Point method.

    Attributes:
        initial (float): Initial guess for the root.
    """
    g_expression: str = Field(..., description="Function g(x) to be used in the fixed point method.")
    initial: float = Field(..., description="Initial value for the fixed point calculation.")

class NewtonRaphsonModel(NumericalMethodRequest):
    """
    Data model for the Newton-Raphson method.

    This model extends the `NumericalMethodRequest` model and adds specific attributes for the Newton-Raphson method.

    Attributes:
        initial (float): Initial guess for the root.
        derivative_expression (Optional[str])
    """
    initial: float = Field(..., description="Initial value for the Newton-Raphson calculation.")
    derivative_expression: Optional[str] = Field(None, description="Derivative expression of the function to be used in the Newton-Raphson method.")

class SecantModel(NumericalMethodRequest):
    """
    Data model for the Secant method.

    This model extends the `NumericalMethodRequest` model and adds specific attributes for the Secant method.

    Attributes:
        initial (float): Initial guess for the root.
        second_initial (float): Second initial guess for the root.
    """
    initial: float = Field(..., description="Initial value for the secant calculation.")
    second_initial: float = Field(..., description="Second initial value for the secant calculation.")

class FirstNewtonModified(NewtonRaphsonModel):
    """
    Data model for the First Modified Newton-Raphson method.

    This model extends the `NewtonRaphsonModel` model and adds specific attributes for the First Modified Newton-Raphson method.

    Attributes:
        multiplicity (int): Multiplicity of the multiple root.
    """
    multiplicity: int = Field(..., description="Multiplicity of the multiple root.")

class SecondNewtonModified(NewtonRaphsonModel):
    """
    Data model for the Second Modified Newton-Raphson method.

    This model extends the `NewtonRaphsonModel` model and adds specific attributes for the Second Modified Newton-Raphson method.

    Attributes:
        second_derivative_expression (Optional[str])
    """
    second_derivative_expression: Optional[str] = Field(None, description="Second derivative expression of the function to be used in the Second Modified Newton-Raphson method.")


class SpectralAndConvergenceResponse(BaseModel):
    """
    Data model for spectral radius and convergence responses.

    This model is used for spectral radius and convergence responses. It contains the `spectral_radius` attribute, which represents the spectral radius of the matrix, and the `convergence` attribute, which indicates whether the method converges or not.

    Attributes:
        spectral_radius (str): Spectral radius of the matrix.
        convergence (str): Message indicating whether the method converges or not.
    """
    spectral_radius: str = Field(description="Spectral radius of the matrix.")
    convergence: str = Field(description="Message indicating whether the method converges or not.")

class EquationSystemsRequest(BaseModel):
    """
    Data model for equation systems requests.

    This model is used for equation systems requests. It contains the `A` attribute, which represents the matrix of coefficients, the `b` attribute, which represents the vector of solutions, and the `n` attribute, which represents the number of equations.
    
    Attributes:
        A (List[List[float]]): Matrix of coefficients of the system of equations.
        b (List[List[float]]): Vector of solutions of the system of equations.
        precision (int): Number of decimal places to round the values.
        order (int): Positive integer which indicates the order of the norm used to calculate the error, 0
    """
    A: List[List[float]] = Field(..., description="Matrix of coefficients of the system of equations.")
    b: List[List[float]] = Field(..., description="Vector of solutions of the system of equations.")
    precision: int = Field(16, description="Number of decimal places to round the values.")
    order: int = Field(0, description="Positive integer which indicates the order of the norm used to calculate the error, 0 for infinite norm")


class GaussEliminationRequest(EquationSystemsRequest):
    """
    Data model for the Gauss Elimination method.

    This model extends the `EquationSystemsRequest` model and adds specific attributes for the Gauss Elimination method.
    
    Attributes:
        pivot_type (Optional[int]): Type of pivot to be used in the method. Default is None and just can take the 1 and 2 values.
        n (Optional[int]): Number of equations in the system.
    """
    pivot_type: Optional[Literal[1, 2]] = Field(None, description="Type of pivot to be used in the method. Default is None and just can take the 1 and 2 values.")
    n: Optional[int] = Field(None, description="Number of equations in the system.")

class EquationSystemsResponse(BaseModel):
    """
    Data model for equation systems responses.

    This model is used for equation systems responses. It contains the `x` attribute, which represents the solutions of the system of equations.
    
    Attributes:
        x (List[float]): List of the solutions of the system of equations.
    """
    x: List[List[str]] = Field(description="List of the solutions of the system of equations.")

class GaussEliminationResponse(EquationSystemsResponse):
    """
    Data model for the Gauss Elimination method response.

    This model is used for the Gauss Elimination method response.
    
    Attributes:
        vectorial_error (List[List[str]]): List of the vectorial errors of the system of  solution by gauss elimination.
        absolute_error (str): Absolute error of the system of equations solution by gauss elimination.
    """
    vectorial_error: List[List[str]] = Field(description="List of the vectorial errors of the system of  solution by gauss elimination.")
    absolute_error: str = Field(description="Absolute error of the system of equations solution by gauss elimination.")


class LUFactorizationRequest(EquationSystemsRequest):
    """
    Data model for the LU Factorization method.

    This model extends the `EquationSystemsRequest` model and adds specific attributes for the LU Factorization method.

    Attributes:
        pivot_type (Optional[int]): Type of pivot to be used in the method. Default is None and just can take the 1 and 2 values.
        n (Optional[int]): Number of equations in the system.
    """
    pivot_type: Optional[Literal[1]] = Field(None, description="Type of pivot to be used in the method. Default is None and just can take the 1 value.")
    n: Optional[int] = Field(None, description="Number of equations in the system.")


class LUFactorizationResponse(EquationSystemsResponse):
    """
    Data model for the LU Factorization method response.

    This model is used for the LU Factorization method response.

    Attributes:
        vectorial_error (List[List[str]]): List of the vectorial errors of the system of  solution by gauss elimination.
        absolute_error (str): Absolute error of the system of equations solution by gauss elimination.
        L (List[List[str]]): Lower triangular matrix of the LU factorization.
        U (List[List[str]]): Upper triangular matrix of the LU factorization.
    """
    vectorial_error: List[List[str]] = Field(description="List of the vectorial errors of the system of  solution by gauss elimination.")
    absolute_error: str = Field(description="Absolute error of the system of equations solution by gauss elimination.")
    L: List[List[str]] = Field(description="Lower triangular matrix of the LU factorization.")
    U: List[List[str]] = Field(description="Upper triangular matrix of the LU factorization.")


class IterativeMatrixEquationSystemResponse(BaseModel):
    """
    Data model for iterative matrix equation system responses.

    This model is used for iterative matrix equation system responses. It contains the `x` attribute, which represents the solutions of the system of equations.

    Attributes:
        iterations (List[int]): List of the number of iterations taken to reach the result.
        x (List[List[str]]): List of the solutions of the system of equations.
        error (List[str]): List of the errors at each iteration.
        message (str): Message to be displayed to the user
    """
    iterations: List[int] = Field(description="List of the number of iterations taken to reach the result.")
    x: List[List[str]] = Field(description="List of the solutions of the system of equations.")
    error: List[str] = Field(description="List of the errors at each iteration.")
    message: str = Field(description="Message to be displayed to the user.")

class IterativeMatrixEquationSystemRequest(EquationSystemsRequest):
    """
    Data model for iterative matrix equation system requests.

    This model extends the `EquationSystemsRequest` model and adds specific attributes for iterative matrix equation system methods.

    Attributes:
        tol (float): Tolerance for the solution.
        max_iter (int): Maximum number of iterations.
        error_type (str): Type of error to be used in the method
        method_type (str): Type of iterative or matrix method to be used.
    """
    tol: float = Field(..., description="Tolerance for the solution.")
    max_iter: int = Field(100, description="Maximum number of iterations.")
    error_type: Literal["absolute", "relative"] = Field("absolute", description="Type of error to be used in the method.")
    x_initial: List[List[float]] = Field(..., description="Initial guess for the solution.")
    method_type: Literal["iterative", "matrix"] = Field("matrix", description="Type of iterative or matrix method to be used.")


class SorRequest(IterativeMatrixEquationSystemRequest):
    """
    Data model for the SOR method.

    This model extends the `IterativeMatrixEquationSystemRequest` model and adds specific attributes for the SOR method.

    Attributes:
        omega (float): Relaxation factor.
    """
    # Omega, but sent as w by users
    omega: float = Field(..., description="Relaxation factor.", alias="w")


class InterpolationRequest(BaseModel):
    """
    Data model for interpolation requests.

    This model is used for interpolation requests. It contains the `x` attribute, which represents the x values, and the `y` attribute, which represents the y values.

    Attributes:
        x (List[float]): List of x values.
        y (List[float]): List of y values.
        precision (int): Number of decimal places to round the values.
    """
    x: List[float] = Field(..., description="List of x values.")
    y: List[float] = Field(..., description="List of y values.")
    precision: int = Field(16, description="Number of decimal places to round the values.")


class InterpolationResponse(BaseModel):
    """
    Data model for interpolation responses.
    
    This model is used for interpolation responses. It contains the `polynomial` attribute, which represents the polynomial obtained from the interpolation.

    Attributes:
        polynomial (str): Polynomial obtained from the interpolation.
        coefficients (List[str]): List of coefficients of the polynomial.
    """
    polynomial: str = Field(description="Polynomial obtained from the interpolation.")
    coefficients: List[str] = Field(description="List of coefficients of the polynomial.")
    
    
class VandermondeResponse(InterpolationResponse):
    """
    Data model for Vandermonde responses.
    
    This model is used for Vandermonde responses. It contains the `vandermonde_matrix` attribute, which represents the Vandermonde matrix obtained from the interpolation.

    Attributes:
        vandermonde_matrix (List[List[str]]): List of the Vandermonde matrix.
    """
    vandermonde_matrix: List[List[str]] = Field(description="List of the Vandermonde matrix.")
    
    
class NewtonResponse(InterpolationResponse):
    """
    Data model for Newton responses.
    
    This model is used for Newton responses. It contains the `difference_table` attribute, which represents the difference table obtained from the interpolation.

    Attributes:
        difference_table (List[List[str]]): List of the difference table.
    """
    difference_table: List[List[str]] = Field(description="List of the difference table.")
    
    
class SplineRequest(InterpolationRequest):
    """
    Data model for spline requests.

    This model extends the `InterpolationRequest` model and adds specific attributes for spline methods.

    Attributes:
        degree (int): Type of spline method to be used.
    """
    degree: Literal[1, 3] = Field(1, description="Type of spline method to be used.")
    
    
class SplineFunction(BaseModel):
    """
    Data model for spline functions responses.
    
    This model is used for spline function responses. It contains the `function` attribute, which represents the function obtained from the spline method and the interval of the function.
    
    Attributes:
        function (str): Function obtained from the spline method.
        interval (str): Interval of the function.
    """
    function: str = Field(description="Function obtained from the spline method.")
    interval: str = Field(description="Interval of the function.")
    
    
class SplineResponse(BaseModel):
    """
    Data model for spline responses.
    
    This model is used for spline responses. It contains the `functions` attribute, which represents the functions obtained from the spline method.

    Attributes:
        functions (List[str]): List of functions obtained from the spline method.
        coefficients (List[List[str]]): List of coefficients of the functions.
    """
    functions: List[SplineFunction] = Field(description="List of functions obtained from the spline method.")
    coefficients: List[List[str]] = Field(description="List of coefficients of the functions.")
    