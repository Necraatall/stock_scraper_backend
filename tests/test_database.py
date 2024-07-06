# tests/test_database.py
import pytest
from src.scraper import save_stock_data, get_stock_data
from src.models import Base, Stock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use DATABASE_URL for Postgresql database
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()

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
        assert 'time' in data or data.get('time') is None

def test_save_stock_data(setup_database, db_session):
    """Test to check if scraped stock data is saved to the database."""
    save_stock_data()
    
    # Verify data is saved in the main table
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
        assert stock.change_time is not None
