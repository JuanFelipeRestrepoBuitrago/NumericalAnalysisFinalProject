from sqlalchemy import Column, Integer, String
from app.config.database import Base

class User(Base):
    """
    Class that represents the users table in the database.

    Attributes:
        id (int) : The user's unique identifier.
        username (str) : The user's username.
        password (str) : The user's password.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
