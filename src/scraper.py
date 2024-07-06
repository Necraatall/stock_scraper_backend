# src/scraper.py
import os
from sqlalchemy import (
  Table, 
  MetaData, 
  Column, 
  Integer, 
  String, 
  Float, 
  DateTime, 
  create_engine)
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.models import Stock, Base

# Load environment variables
load_dotenv()

# Set DATABASE_URL based on the TESTING environment variable
if os.getenv('TESTING') == 'true':
    DATABASE_URL = os.getenv('TEST_DATABASE_URL')
else:
    DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Fetch page content
def fetch_page_content(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Parse HTML content
def parse_html(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'class': 'pd huste leftcolumnwidth r rowcl'})
    if table is None:
        raise ValueError("Could not find the stock table on the page")
    return table

# Extract rows from table
def extract_rows(table) -> list:
    return table.find_all('tr')[1:]  # Skip the header row

# Parse float value
def parse_float(text: str) -> float:
    try:
        return float(text.replace(',', ''))
    except ValueError:
        return 0.0  # or any default value

# Parse integer value
def parse_int(text: str) -> int:
    try:
        return int(text.replace(' ', '').replace(',', ''))
    except ValueError:
        return 0  # or any default value

# Parse row data
def parse_row(row) -> dict:
    columns = row.find_all('td')
    if len(columns) < 8:
        return {}  # Skip incomplete rows and return empty dict
    
    name_td = columns[0].find('a')
    if name_td is None or 'title' not in name_td.attrs:
        return {}  # Skip rows with invalid name column and return empty dict
    
    stock = {
        "name": name_td['title'],
        "price": parse_float(columns[1].text.strip()) if columns[1].text.strip() else 0.0,
        "change": columns[2].text.strip() if len(columns) > 2 else "",
        "volume": parse_int(columns[3].text.strip()) if columns[3].text.strip() else 0,
        "buy": parse_float(columns[4].text.strip()) if columns[4].text.strip() else 0.0,
        "sell": parse_float(columns[5].text.strip()) if columns[5].text.strip() else 0.0,
        "min": parse_float(columns[6].text.strip()) if columns[6].text.strip() else 0.0,
        "max": parse_float(columns[7].text.strip()) if columns[7].text.strip() else 0.0,
        "change_time": columns[8].text.strip() if len(columns) > 8 else None,
    }
    return stock

# Get stock data from webpage
def get_stock_data() -> list:
    url = "https://www.kurzy.cz/akcie-cz/burza/"
    html_content = fetch_page_content(url)
    table = parse_html(html_content)
    rows = extract_rows(table)

    stock_data = []
    for row in rows:
        stock = parse_row(row)
        if stock:
            stock_data.append(stock)
    
    return stock_data

# Create stock table
def create_stock_table(original_name: str):
    table_name = original_name.replace("akcie_", "other_stocks_").split(",")[0].replace(" ", "_").lower()
    market_value = original_name.split('_')[-1]
    stock_type_value = original_name.split('_')[0].replace("_", " ")

    table = Table(
        table_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('date', DateTime, default=datetime.now(timezone.utc)),
        Column('price', Float),
        Column('volume', Integer),
        Column('min', Float),
        Column('max', Float),
        Column('market', String, default=market_value),
        Column('stock_type', String, default=stock_type_value),
        extend_existing=True
    )
    metadata.create_all(engine)  # Create the table if it doesn't exist
    return table

# Save stock data to database
def save_stock_data():
    session = SessionLocal()
    Base.metadata.create_all(bind=engine)  # Ensure the main stocks table exists
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
            change_time=data["change_time"],
            record_time=datetime.now(timezone.utc)
        )
        session.add(stock)

        # Create a new table for the stock if it doesn't exist
        original_name = data["name"]
        stock_table = create_stock_table(original_name)

        # Insert data into the stock-specific table
        insert_statement = stock_table.insert().values(
            date=datetime.now(timezone.utc),
            price=data["price"],
            volume=data["volume"],
            min=data["min"],
            max=data["max"],
            market="online burza",
            stock_type="akcie"
        )
        session.execute(insert_statement)
    
    session.commit()
    session.close()
