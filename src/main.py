# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from scraper import save_stock_data, Stock as StockModel, SessionLocal, Base, engine
from models import Stock, StockCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/scrape")
def scrape_data(db: Session = Depends(get_db)):
    save_stock_data()
    return {"message": "Data scraped and saved successfully"}

@app.get("/stocks", response_model=list[Stock])
def get_stocks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stocks = db.query(StockModel).offset(skip).limit(limit).all()
    return stocks

@app.post("/stocks", response_model=Stock)
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    db_stock = StockModel(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


# ###################### jede
# from fastapi import FastAPI  
# app = FastAPI()   
# @app.get("/") 
# async def main_route():     
#   return {"message": "Hey, It is me Goku"}