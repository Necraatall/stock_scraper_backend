# src/models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from pydantic import BaseModel
from datetime import datetime, timezone

Base = declarative_base()

class Stock(Base):
    """
    Represents a stock record in the database.
    """
    __tablename__ = "stocks"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    price: float = Column(Float)
    change: str = Column(String)
    volume: int = Column(Integer)
    buy: float = Column(Float)
    sell: float = Column(Float)
    min: float = Column(Float)
    max: float = Column(Float)
    record_time: datetime = Column(DateTime, default=datetime.now(timezone.utc))
    change_time: str = Column(String)

class StockBase(BaseModel):
    """
    Base model for Stock used for validation.
    """
    name: str
    price: float
    change: str
    volume: int
    buy: float
    sell: float
    min: float
    max: float
    change_time: str

class StockCreate(StockBase):
    """
    Model for creating a new Stock.
    """
    pass

class StockSchema(StockBase):
    """
    Schema for displaying a Stock with ID and record time.
    """
    id: int
    record_time: datetime

    class Config:
        orm_mode: True
