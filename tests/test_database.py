# tests/test_database.py
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from src.models import Base, Stock
from src.scraper import save_stock_data, get_stock_data

# Database URL for testing
DATABASE_URL = "sqlite:///:memory:"

# SQLAlchemy engine and session setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    """Setup the database for testing."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    session = SessionLocal()
    yield session
    session.close()

def test_database_connection():
    """Test to check if the database connection is successful."""
    try:
        connection = engine.connect()
        assert not connection.closed, "Failed to open database connection"
    except OperationalError:
        pytest.fail("Unable to connect to the database")
    finally:
        connection.close()
        assert connection.closed, "Failed to close the database connection"

def test_get_stock_data():
    """Test to check if stock data is scraped successfully."""
    stock_data = get_stock_data()
    assert len(stock_data) > 0, "No stock data scraped"
    for data in stock_data:
        assert 'name' in data
        assert 'price' in data
        assert 'change' in data
        assert 'volume' in data
        assert 'buy' in data
        assert 'sell' in data
        assert 'min' in data
        assert 'max' in data
        assert 'time' in data or data['time'] is None

def test_save_stock_data(setup_database, db_session):
    """Test to check if scraped stock data is saved to the database."""
    save_stock_data()
    stocks = db_session.query(Stock).all()
    assert len(stocks) > 0, "No stock data saved to the database"
    for stock in stocks:
        assert stock.name is not None
        assert stock.price is not None
        assert stock.change is not None
        assert stock.volume is not None
        assert stock.buy is not None
        assert stock.sell is not None
        assert stock.min is not None
        assert stock.max is not None
        assert stock.time is not None
