from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
import logging
from sqlalchemy.orm import Session

# Configuration, models, methods and authentication modules imports
from app.config.database import get_db
from app.config.limiter import limiter
from app.config.env import API_NAME
from app.models.models import ResponseError, UserLogin, UserLoginResponse
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception
from app.utils.crud import get_user_by_username

router = APIRouter()

# Log file name
log_filename = f"api_{API_NAME}.log"

# Configurate the logging level to catch all messages from DEBUG onwards
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    handlers=[logging.FileHandler(log_filename),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)

@router.get('/',
            tags=["Root"],
            status_code=status.HTTP_200_OK,
            summary="Root endpoint.",
            response_model=str,
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."}
            })
@limiter.limit("1/minute")
def root(request: Request):
    """
    Root endpoint.

    Returns:
        (str): Welcome message.
    """
    try:
        logger.info("Root endpoint.")
        return "Welcome to the Backend Numerical Methods API!"
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        raise_exception(e, logger)

@router.post('/login/',
                tags=["Authentication"],
                status_code=status.HTTP_200_OK,
                summary="User login.",
                response_model=UserLoginResponse,
                responses={
                    500: {"model": ResponseError, "description": "Internal server error."},
                    429: {"model": ResponseError, "description": "Too many requests."}
                })
@limiter.limit("20/minute")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    """
    User login endpoint.

    Args:
        user (UserLogin): User credentials.

    Returns:
        (UserLoginResponse): JWT token.

    Raises:
        HTTPException: If the user is not found or the password is incorrect.
    """
    try:
        logger.info(f"User login attempt for {user.username}.")
        # Fetch user from the database
        db_user = get_user_by_username(db, user.username)

        # Verify user and password match
        if not db_user or not auth_handler.verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail='Invalid username or password')
        
        # Generate token
        token = auth_handler.create_token({'username': db_user.username})

        logger.info(f"User {user.username} successfully logged in.")
        # Return token
        return UserLoginResponse(access_token=token, token_type="Bearer")
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        raise_exception(e, logger)


@router.get('/protected/',
            tags=["Protected"],
            status_code=status.HTTP_200_OK,
            summary="Protected endpoint to test authentication.",
            response_model=str,
            responses={
                500: {"model": ResponseError, "description": "Internal server error."},
                429: {"model": ResponseError, "description": "Too many requests."}
            })
@limiter.limit("1/minute")
def protected(request: Request, auth: dict = Depends(auth_handler.authenticate)):
    """
    Root endpoint.

    Returns:
        (str): Welcome message.
    """
    try:
        logger.info("Protected endpoint.")
        return f"This is a protected endpoint. Welcome, {auth['username']}!"
    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Too many requests.")
    except Exception as e:
        raise_exception(e, logger)
        