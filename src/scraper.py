# app/scraper.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.models import Stock, Base

# Načtení proměnných prostředí
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_stock_data():
    url = "https://www.kurzy.cz/akcie-cz/burza/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', {'class': 'stock-table'})
    rows = table.find_all('tr')[1:]  # Skip the header row

    stock_data = []

    for row in rows:
        columns = row.find_all('td')
        if len(columns) < 9:
            continue  # Skip incomplete rows
        
        stock = {
            "name": columns[0].text.strip(),
            "price": float(columns[1].text.strip().replace(',', '')),
            "change": columns[2].text.strip(),
            "volume": int(columns[3].text.strip().replace(' ', '').replace(',', '')),
            "buy": float(columns[4].text.strip().replace(',', '')),
            "sell": float(columns[5].text.strip().replace(',', '')),
            "min": float(columns[6].text.strip().replace(',', '')),
            "max": float(columns[7].text.strip().replace(',', '')),
            "change_time": columns[8].text.strip()
        }
        
        stock_data.append(stock)

    return stock_data

def save_stock_data():
    session = SessionLocal()
    stock_data = get_stock_data()

    for data in stock_data:
        stock = Stock(
            name=data["name"],
            price=data["price"],
            change=data["change"],
            volume=data["volume"],
            buy=data["buy"],
            sell=data["sell"],
            min=data["min"],
            max=data["max"],
            change_time=data["change_time"]
        )
        session.add(stock)
    
    session.commit()
    session.close()
