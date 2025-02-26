from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config.setting import settings

# Database URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
