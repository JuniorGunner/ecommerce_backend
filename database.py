from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy database URL. For PostgreSQL, it might look like:
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/dbname"
SQLALCHEMY_DATABASE_URL = "postgresql://admin:3c0mm3rc3@db/ecommerce_db"

# Create a SQLAlchemy engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal class is a factory for creating new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()
