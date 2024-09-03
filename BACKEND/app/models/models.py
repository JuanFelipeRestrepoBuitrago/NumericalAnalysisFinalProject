from typing import Optional
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
