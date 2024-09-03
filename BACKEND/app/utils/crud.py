from sqlalchemy.orm import Session
from app.models.db_models import User
from app.auth.auth import auth_handler
from app.config.env import DEFAULT_USER_NAME, DEFAULT_USER_PASSWORD
from app.models.db_models import User
from app.config.database import engine, Base, SessionLocal


def init_db():
    """
    Initialize the database with some initial data

    Arguments:
        db (Session) : The database session
    """
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    # Create a database session
    db = SessionLocal()
    try:
        # Check if the default user exists
        user = get_user_by_username(db, DEFAULT_USER_NAME)
        if not user:
            # Create the default user
            create_user(db, DEFAULT_USER_NAME, DEFAULT_USER_PASSWORD)
            print(f"Default user '{DEFAULT_USER_NAME}' created.")
        else:
            print(f"Default user '{DEFAULT_USER_NAME}' already exists.")
    finally:
        db.close()


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


def create_user(db: Session, username: str, password: str) -> User:
    """
    Create a user with a username and password

    Arguments:
        db (Session) : The database session
        username (str) : The username of the user
        password (str) : The password of the user

    Returns:
        (User): The created user
    """
    # Hash or encrypt the password before storing it
    hashed_password = auth_handler.hash_password(password)

    # Create the user
    user = User(username=username, password=hashed_password)
    # Add the user to the database
    db.add(user)
    # Commit the changes to the database
    db.commit()
    # Refresh the user to get the updated id
    db.refresh(user)
    return user
