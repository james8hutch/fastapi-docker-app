import os
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import Base, get_db, TEST_DATABASE_URL
import sys

# Remove existing test database file (ensures a fresh start for tests)
db_path = TEST_DATABASE_URL.replace("sqlite:///", "")
if os.path.exists(db_path):
    os.remove(db_path)

# Create a separate engine and sessionmaker for the SQLite test database
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override the `get_db` dependency for testing
def override_get_db():
    db = TestSessionLocal()
    
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create the database schema for the SQLite test database at the start
    of the test session and drop it afterward.
    """
    # Ensure the database file is removed before running tests
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create the database schema
    Base.metadata.create_all(bind=test_engine)
    time.sleep(1)  # Delay to ensure the DB is ready
    
    yield

    Base.metadata.drop_all(bind=test_engine)
    if os.path.exists(db_path):
        os.remove(db_path)  # Ensure cleanup

@pytest.fixture(scope="function")
def test_db_session(setup_test_db):
    """
    Provide a transactional database session for each test function.
    Ensures a fresh state for every test by rolling back at the end.
    """
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="module")
def client(setup_test_db):
    """
    Provide a TestClient instance for testing API endpoints.
    This fixture ensures the database schema is set up before tests run.
    """
    return TestClient(app)

def print_tables(session):
    """
    Print the list of tables in the database and their row counts.
    """
    inspector = inspect(session.bind)
    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")
    for table in tables:
        count = session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"JH {table}: {count} rows")
