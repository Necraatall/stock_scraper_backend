# tests/test_healthcheck.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Use DATABASE_URL for PostgreSQL database
DATABASE_URL = os.getenv("DATABASE_URL")

@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine(DATABASE_URL)
    yield engine
    engine.dispose()

def test_database_connection(db_engine):
    """Test to check if the database connection is successful."""
    try:
        connection = db_engine.connect()
        assert not connection.closed, "Failed to open database connection"
    except OperationalError:
        pytest.fail("Unable to connect to the database")
    finally:
        connection.close()
        assert connection.closed, "Failed to close the database connection"

def test_database_creation(db_engine):
    """Test to check if the expected table 'users' exists in the database."""
    try:
        connection = db_engine.connect()
        result = connection.execute(
            "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
        tables = [row[0] for row in result]
        assert 'users' in tables, "Table 'users' was not found in the database"
    except OperationalError:
        pytest.fail("Unable to connect to the database")
    finally:
        connection.close()
        assert connection.closed, "Failed to close the database connection"
