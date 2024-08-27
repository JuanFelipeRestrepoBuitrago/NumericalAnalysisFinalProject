from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from app.config.env import DATABASE_URL

# Create a database instance and an engine instance
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

# Create a session instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a metadata instance and a base instance so that the models can inherit from it
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Create a function to get a database session
def get_db():
    """
    Get a database session to interact with the database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
