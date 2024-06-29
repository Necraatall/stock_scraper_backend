# test/test_scraper
import requests
from bs4 import BeautifulSoup
import pytest

def fetch_page_content(url):
    response = requests.get(url)
    return response.text

def parse_stock_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'class': 'pd huste leftcolumnwidth r rowcl'})
    if table is None:
        raise ValueError("Could not find the stock table on the page")
    return table

def extract_rows(table):
    rows = table.find_all('tr')[1:]
    if len(rows) == 0:
        raise ValueError("The stock table is empty")
    return rows

def extract_data_from_row(row):
    cols = row.find_all('td')
    if len(cols) < 8:
        raise ValueError("Row does not contain enough data")

    name_td = cols[0].find('a')
    if name_td is None or 'title' not in name_td.attrs:
        raise ValueError("Name column does not contain a valid title attribute")

    name = name_td['title']
    if not name:
        raise ValueError("Name extracted from title is empty")

    return {
        'name': name,
        'price': cols[1].text.strip(),
        'change': cols[2].text.strip(),
        'volume': cols[3].text.strip(),
        'buy': cols[4].text.strip(),
        'sell': cols[5].text.strip(),
        'min': cols[6].text.strip(),
        'max': cols[7].text.strip(),
        'time': cols[8].text.strip() if len(cols) > 8 else None,  # Some rows might not have this column
    }

def extract_stock_data(table):
    rows = extract_rows(table)
    stock_data_list = [extract_data_from_row(row) for row in rows]
    return stock_data_list

def test_stock_table_exists():
    url = "https://www.kurzy.cz/akcie-cz/burza/bcpp_online"
    html_content = fetch_page_content(url)
    table = parse_stock_table(html_content)
    stock_data_list = extract_stock_data(table)

    # Print the extracted data
    for stock_data in stock_data_list:
        print(stock_data)



# # src/test_scraper.py
# import sys
# import os
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from src.models import Base, Stock

# # Přidání cesty k modulu app do sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# # Nastavení proměnné prostředí DATABASE_URL na SQLite pro testování
# DATABASE_URL = "sqlite:///:memory:"

# from src.scraper import save_stock_data, get_stock_data

# # Funkce pro získání databázové URL, umožňující přepsání v testovacím prostředí
# def get_database_url():
#     return os.getenv('DATABASE_URL', 'postgresql://postgres:root@db:5432/stock_db')

# # Použití get_database_url pro nastavení testovací databáze pomocí SQLite in-memory
# DATABASE_URL = get_database_url()
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="module")
# def setup_database():
#     # Vytvoření tabulek v testovací databázi
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)

# @pytest.fixture(scope="function")
# def db_session():
#     session = SessionLocal()
#     yield session
#     session.close()

# def test_get_stock_data():
#     stock_data = get_stock_data()
#     assert len(stock_data) > 0, "No stock data scraped"
#     for data in stock_data:
#         assert 'name' in data
#         assert 'price' in data
#         assert 'change' in data
#         assert 'volume' in data
#         assert 'buy' in data
#         assert 'sell' in data
#         assert 'min' in data
#         assert 'max' in data
#         assert 'change_time' in data

# def test_save_stock_data(setup_database, db_session):
#     # Uložení scrapovaných dat do testovací databáze
#     save_stock_data()
    
#     # Kontrola, zda jsou data v databázi
#     stocks = db_session.query(Stock).all()
#     assert len(stocks) > 0, "No stock data saved to the database"
#     for stock in stocks:
#         assert stock.name is not None
#         assert stock.price is not None
#         assert stock.change is not None
#         assert stock.volume is not None
#         assert stock.buy is not None
#         assert stock.sell is not None
#         assert stock.min is not None
#         assert stock.max is not None
#         assert stock.change_time is not None

# # Spuštění testů
# if __name__ == "__main__":
#     pytest.main()

