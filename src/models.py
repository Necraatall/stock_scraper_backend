# app/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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

class Stock(StockBase):
    id: int
    record_time: datetime

    class Config:
        orm_mode: True
