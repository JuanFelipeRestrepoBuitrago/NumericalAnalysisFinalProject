import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from typing import Union

# Importing JWT_SECRET from the configuration module
from app.config.env import JWT_SECRET

class AuthenticationHandler:
    """Handles user authentication operations."""
    
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hashes the password using bcrypt.
        
        Args:
        - password (str): Plain text password.
        
        Returns:
        - str: Hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a password against its hashed version.
        
        Args:
        - plain_password (str): Plain text password.
        - hashed_password (str): Hashed version of the password.
        
        Returns:
        - bool: True if verification is successful, False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_token(self, user: dict) -> str:
        """Generates a JWT token for the given user_id.
        
        Args:
        - user_id (str): Unique identifier for the user.
        
        Returns:
        - str: JWT token.
        """
        expiration = datetime.utcnow() + timedelta(days=2)
        payload = {
            'exp': expiration,
            'iat': datetime.utcnow(),
            'user': user  # Storing entire user object in the token
        }
        return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    def decode_token(self, token: str) -> Union[dict, None]:
        """Decodes a JWT token and returns its payload.
        
        Args:
        - token (str): JWT token.
        
        Returns:
        - dict: User dict if verification is successful.
        
        Raises:
        - HTTPException: If token is expired or invalid.
        """
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return payload['user']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def authenticate(self, auth_credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
        """Wrapper function for token authentication.
        
        Args:
        - auth_credentials (HTTPAuthorizationCredentials): HTTP authorization credentials.
        
        Returns:
        - str: User ID if authentication is successful.
        
        Raises:
        - HTTPException: If token is expired or invalid.
        """
        return self.decode_token(auth_credentials.credentials)

# Instantiate the authentication handler for further use
auth_handler = AuthenticationHandler()