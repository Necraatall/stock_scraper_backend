# app/models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from pydantic import BaseModel
from datetime import datetime, timezone

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    change = Column(String)
    volume = Column(Integer)
    buy = Column(Float)
    sell = Column(Float)
    min = Column(Float)
    max = Column(Float)
    record_time = Column(DateTime, default=datetime.now(timezone.utc))
    change_time = Column(String)

class StockBase(BaseModel):
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
    pass

class StockSchema(StockBase):
    id: int
    record_time: datetime

    class Config:
        orm_mode: True
