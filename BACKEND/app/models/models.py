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
        email (Optional[str]): Email address of the user.
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
        error_type (Optional[str]): Type of error to be used in the method.
        tolerance (float): Tolerance value for the error in the method.
        max_iterations (int): Maximum number of iterations for the method.
        precision (int): Number of decimal places to round the values.
    """
    expression: str = Field(..., description="Mathematical expression or function to be evaluated.")
    error_type: Optional[Literal["absolute", "relative"]] = Field("absolute", description="Type of error to be used in the method.")
    tolerance: float = Field(..., description="Tolerance value for the error in the method.")
    max_iterations: int = Field(..., description="Maximum number of iterations for the method.")
    precision: Optional[int] = Field(16, description="Number of decimal places to round the values.")

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
