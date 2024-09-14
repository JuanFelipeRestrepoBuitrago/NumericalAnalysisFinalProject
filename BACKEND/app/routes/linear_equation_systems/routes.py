from fastapi import APIRouter, HTTPException, Request, Depends, status
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

# Configuration, models, methods and authentication modules imports
from app.config.limiter import limiter
from app.models.models import ResponseError
from app.auth.auth import auth_handler
from app.utils.utils import raise_exception, parse_expression
from app.routes.routes import logger

router = APIRouter()