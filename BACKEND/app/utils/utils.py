from logging import Logger
from fastapi import HTTPException, status

def raise_exception(e: Exception, logger: Logger):
    """
    Raise an HTTPException and log the error
    """
    logger.error(f"Error : {str(e)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )
