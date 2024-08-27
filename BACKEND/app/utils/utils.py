from logging import Logger
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.db_models import User

def raise_exception(e: Exception, logger: Logger):
    """
    Raise an HTTPException and log the error

    Arguments:
        e (Exception) : The exception that was raised
        logger (Logger) : The logger instance to log

    Raises:
        HTTPException : The HTTPException with the error message
    """
    logger.error(f"Error : {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )

def get_user_by_username(db: Session, username: str) -> User:
    """
    Get a user by their username

    Arguments:
        db (Session) : The database session
        username (str) : The username of the user

    Returns:
        User : The user with the given username
    """
    return db.query(User).filter(User.username == username).first()
