from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
import os

# Environment variable for production database URL (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydb")

# Test database URL (SQLite in-memory database for testing purposes)
TEST_DATABASE_URL = "sqlite:////tmp/test.db"

# Configure the production database engine
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Configure the test database engine (SQLite in-memory)
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# Create sessionmakers for production and test databases
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Declare the base class for SQLAlchemy models
Base = declarative_base()

# Dependency: Get a database session for the production environment
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function: Get a database session for testing purposes
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
