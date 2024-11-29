# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (For SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # This is a local SQLite file-based DB.

# Create an engine that stores data in the local SQLite file.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a sessionmaker for managing database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
