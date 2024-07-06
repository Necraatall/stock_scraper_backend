# src/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.scraper import save_stock_data, SessionLocal, Base, engine
from src.models import StockCreate, StockSchema, Stock as StockModel
from typing import List, Dict

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/scrape", response_model=Dict[str, str])
def scrape_data(db: Session = Depends(get_db)) -> Dict[str, str]:
    try:
        save_stock_data()
        return {"message": "Stock data scraped and saved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/stocks", response_model=List[StockSchema])
def get_stocks(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
    ) -> List[StockSchema]:
    stocks = db.query(StockModel).offset(skip).limit(limit).all()
    return stocks

@app.post("/stocks", response_model=StockSchema)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)) -> StockSchema:
    db_stock = StockModel(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
