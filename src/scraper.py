# # src/scraper.py
# import os
# from typing import Optional
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone
# from src.models import Stock, Base

# # Načtení proměnných prostředí
# load_dotenv()

# DATABASE_URL = os.getenv('DATABASE_URL')
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def fetch_page_content(url: str) -> str:
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.text

# def parse_html(html_content: str):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     table = soup.find('table', {'class': 'pd huste leftcolumnwidth r rowcl'})
#     if table is None:
#         raise ValueError("Could not find the stock table on the page")
#     return table

# def extract_rows(table) -> list:
#     return table.find_all('tr')[1:]  # Skip the header row

# def parse_float(text: str) -> Optional[float]:
#     try:
#         return float(text.replace(',', ''))
#     except ValueError:
#         return None

# def parse_int(text: str) -> Optional[int]:
#     try:
#         return int(text.replace(' ', '').replace(',', ''))
#     except ValueError:
#         return None

# def parse_row(row) -> Optional[dict]:
#     columns = row.find_all('td')
#     if len(columns) < 8:
#         return None  # Skip incomplete rows
    
#     name_td = columns[0].find('a')
#     if name_td is None or 'title' not in name_td.attrs:
#         return None  # Skip rows with invalid name column
    
#     stock = {
#         "name": name_td['title'],
#         "price": parse_float(columns[1].text.strip()) if columns[1].text.strip() else None,
#         "change": columns[2].text.strip() if len(columns) > 2 else None,
#         "volume": parse_int(columns[3].text.strip()) if columns[3].text.strip() else None,
#         "buy": parse_float(columns[4].text.strip()) if columns[4].text.strip() else None,
#         "sell": parse_float(columns[5].text.strip()) if columns[5].text.strip() else None,
#         "min": parse_float(columns[6].text.strip()) if columns[6].text.strip() else None,
#         "max": parse_float(columns[7].text.strip()) if columns[7].text.strip() else None,
#         "change_time": columns[8].text.strip() if len(columns) > 8 else None,
#     }
#     return stock

# def get_stock_data() -> list:
#     url = "https://www.kurzy.cz/akcie-cz/burza/"
#     html_content = fetch_page_content(url)
#     table = parse_html(html_content)
#     rows = extract_rows(table)

#     stock_data = []
#     for row in rows:
#         stock = parse_row(row)
#         if stock:
#             stock_data.append(stock)
    
#     return stock_data

# def save_stock_data():
#     session = SessionLocal()
#     Base.metadata.create_all(bind=engine)  # Ensure the table exists
#     stock_data = get_stock_data()

#     for data in stock_data:
#         stock = Stock(
#             name=data["name"],
#             price=data["price"],
#             change=data["change"],
#             volume=data["volume"],
#             buy=data["buy"],
#             sell=data["sell"],
#             min=data["min"],
#             max=data["max"],
#             change_time=data["change_time"],
#             record_time=datetime.now(timezone.utc)
#         )
#         session.add(stock)
    
#     session.commit()
#     session.close()









# ###############################################################
# ################# spatne nazvy tabulek ########################
# ###############################################################
# # vytvori tabulku z kazdeho scrapu
# #                               List of relations
# #  Schema |                       Name                       | Type  |  Owner   
# # --------+--------------------------------------------------+-------+----------
# #  public | akcie_deutsche_bank_ag,_online_burza             | table | postgres
# #  public | akcie_e.on_se,_online_burza                      | table | postgres
# #  public | akcie_e4u_a.s.,_online_burza                     | table | postgres
# #  public | akcie_eman_a.s.,_online_burza                    | table | postgres
# #  public | akcie_immofinanz_ag,_online_burza                | table | postgres
# #  public | akcie_karo_leather_a.s.,_online_burza            | table | postgres
# #  public | akcie_nokia,_online_burza                        | table | postgres
# #  public | akcie_orlen,_online_burza                        | table | postgres
# #  public | akcie_rbi,_online_burza                          | table | postgres
# #  public | akcie_rwe_ag,_online_burza                       | table | postgres
# #  public | akcie_tatry_mountain_resorts,_a.s.,_online_burza | table | postgres
# #  public | akcie_voestalpine_ag,_online_burza               | table | postgres
# #  public | akcie_volkswagen_ag,_online_burza                | table | postgres
# #  public | alembic_version                                  | table | postgres
# #  public | stocks                                           | table | postgres
# # (15 rows)

# # stock_db=# select * from akcie_deutche_bank_ag,_online_burza
# # stock_db-# select * from akcie_deutche_bank_ag,_online_burza;
# # ERROR:  syntax error at or near "select"
# # LINE 2: select * from akcie_deutche_bank_ag,_online_burza;
# #         ^
# # stock_db=# select * from akcie_deutsche_bank_ag,_online_burza;
# # ERROR:  relation "akcie_deutsche_bank_ag" does not exist
# # LINE 1: select * from akcie_deutsche_bank_ag,_online_burza;


# # src/scraper.py
# import os
# from sqlalchemy import Table, MetaData
# from sqlalchemy.exc import ProgrammingError
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
# from sqlalchemy.orm import sessionmaker
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone
# from src.models import Stock, Base

# # Load environment variables
# load_dotenv()

# DATABASE_URL = os.getenv('DATABASE_URL')
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# metadata = MetaData()

# def fetch_page_content(url: str) -> str:
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.text

# def parse_html(html_content: str):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     table = soup.find('table', {'class': 'pd huste leftcolumnwidth r rowcl'})
#     if table is None:
#         raise ValueError("Could not find the stock table on the page")
#     return table

# def extract_rows(table) -> list:
#     return table.find_all('tr')[1:]  # Skip the header row

# def parse_float(text: str) -> float:
#     try:
#         return float(text.replace(',', ''))
#     except ValueError:
#         return 0.0  # or any default value

# def parse_int(text: str) -> int:
#     try:
#         return int(text.replace(' ', '').replace(',', ''))
#     except ValueError:
#         return 0  # or any default value

# def parse_row(row) -> dict:
#     columns = row.find_all('td')
#     if len(columns) < 8:
#         return {}  # Skip incomplete rows
    
#     name_td = columns[0].find('a')
#     if name_td is None or 'title' not in name_td.attrs:
#         return {}  # Skip rows with invalid name column
    
#     stock = {
#         "name": name_td['title'],
#         "price": parse_float(columns[1].text.strip()) if columns[1].text.strip() else 0.0,
#         "change": columns[2].text.strip() if len(columns) > 2 else "",
#         "volume": parse_int(columns[3].text.strip()) if columns[3].text.strip() else 0,
#         "buy": parse_float(columns[4].text.strip()) if columns[4].text.strip() else 0.0,
#         "sell": parse_float(columns[5].text.strip()) if columns[5].text.strip() else 0.0,
#         "min": parse_float(columns[6].text.strip()) if columns[6].text.strip() else 0.0,
#         "max": parse_float(columns[7].text.strip()) if columns[7].text.strip() else 0.0,
#         "change_time": columns[8].text.strip() if len(columns) > 8 else None,
#     }
#     return stock

# def get_stock_data() -> list:
#     url = "https://www.kurzy.cz/akcie-cz/burza/"
#     html_content = fetch_page_content(url)
#     table = parse_html(html_content)
#     rows = extract_rows(table)

#     stock_data = []
#     for row in rows:
#         stock = parse_row(row)
#         if stock:
#             stock_data.append(stock)
    
#     return stock_data

# def create_stock_table(table_name: str):
#     table = Table(
#         table_name, metadata,
#         Column('id', Integer, primary_key=True),
#         Column('date', DateTime, default=datetime.now(timezone.utc)),
#         Column('price', Float),
#         Column('volume', Integer),
#         Column('min', Float),
#         Column('max', Float),
#         extend_existing=True
#     )
#     metadata.create_all(engine)  # Create the table if it doesn't exist
#     return table

# def save_stock_data():
#     session = SessionLocal()
#     Base.metadata.create_all(bind=engine)  # Ensure the main stocks table exists
#     stock_data = get_stock_data()

#     for data in stock_data:
#         stock = Stock(
#             name=data["name"],
#             price=data["price"],
#             change=data["change"],
#             volume=data["volume"],
#             buy=data["buy"],
#             sell=data["sell"],
#             min=data["min"],
#             max=data["max"],
#             change_time=data["change_time"],
#             record_time=datetime.now(timezone.utc)
#         )
#         session.add(stock)

#         # Create a new table for the stock if it doesn't exist
#         table_name = data["name"].replace(" ", "_").lower()
#         stock_table = create_stock_table(table_name)

#         # Insert data into the stock-specific table
#         insert_statement = stock_table.insert().values(
#             date=datetime.now(timezone.utc),
#             price=data["price"],
#             volume=data["volume"],
#             min=data["min"],
#             max=data["max"]
#         )
#         session.execute(insert_statement)
    
#     session.commit()
#     session.close()






# # ###############################################################
# # ################# spatne nazvy tabulek ########################
# # ###############################################################
# # # vytvori tabulku z kazdeho scrapu
# # stock_db=# \dt
# #                     List of relations
# #  Schema |             Name             | Type  |  Owner   
# # --------+------------------------------+-------+----------
# #  public | akcie_deutsche_bank_ag       | table | postgres
# #  public | akcie_e.on_se                | table | postgres
# #  public | akcie_e4u_a.s.               | table | postgres
# #  public | akcie_eman_a.s.              | table | postgres
# #  public | akcie_immofinanz_ag          | table | postgres
# #  public | akcie_karo_leather_a.s.      | table | postgres
# #  public | akcie_nokia                  | table | postgres
# #  public | akcie_orlen                  | table | postgres
# #  public | akcie_rbi                    | table | postgres
# #  public | akcie_rwe_ag                 | table | postgres
# #  public | akcie_tatry_mountain_resorts | table | postgres
# #  public | akcie_voestalpine_ag         | table | postgres
# #  public | akcie_volkswagen_ag          | table | postgres
# #  public | alembic_version              | table | postgres
# #  public | stocks                       | table | postgres
# # (15 rows)

# # stock_db=# SELECT * FROM akcie_deutsche_bank_ag LIMIT 1;
# #  id |            date            | price  | volume |  min   |  max  | type  |    market    
# # ----+----------------------------+--------+--------+--------+-------+-------+--------------
# #   1 | 2024-06-28 18:52:44.417606 | 371.75 |      0 | 370.45 | 374.9 | akcie | online burza
# # (1 row)

# import os
# from sqlalchemy import Table, MetaData, Column, Integer, String, Float, DateTime
# from sqlalchemy.exc import ProgrammingError
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import requests
# from bs4 import BeautifulSoup
# from datetime import datetime, timezone
# from src.models import Stock, Base

# # Load environment variables
# load_dotenv()

# DATABASE_URL = os.getenv('DATABASE_URL')
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# metadata = MetaData()

# def fetch_page_content(url: str) -> str:
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.text

# def parse_html(html_content: str):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     table = soup.find('table', {'class': 'pd huste leftcolumnwidth r rowcl'})
#     if table is None:
#         raise ValueError("Could not find the stock table on the page")
#     return table

# def extract_rows(table) -> list:
#     return table.find_all('tr')[1:]  # Skip the header row

# def parse_float(text: str) -> float:
#     try:
#         return float(text.replace(',', ''))
#     except ValueError:
#         return 0.0  # or any default value

# def parse_int(text: str) -> int:
#     try:
#         return int(text.replace(' ', '').replace(',', ''))
#     except ValueError:
#         return 0  # or any default value

# def parse_row(row) -> dict:
#     columns = row.find_all('td')
#     if len(columns) < 8:
#         return {}  # Skip incomplete rows and return empty dict
    
#     name_td = columns[0].find('a')
#     if name_td is None or 'title' not in name_td.attrs:
#         return {}  # Skip rows with invalid name column and return empty dict
    
#     stock = {
#         "name": name_td['title'],
#         "price": parse_float(columns[1].text.strip()) if columns[1].text.strip() else 0.0,
#         "change": columns[2].text.strip() if len(columns) > 2 else "",
#         "volume": parse_int(columns[3].text.strip()) if columns[3].text.strip() else 0,
#         "buy": parse_float(columns[4].text.strip()) if columns[4].text.strip() else 0.0,
#         "sell": parse_float(columns[5].text.strip()) if columns[5].text.strip() else 0.0,
#         "min": parse_float(columns[6].text.strip()) if columns[6].text.strip() else 0.0,
#         "max": parse_float(columns[7].text.strip()) if columns[7].text.strip() else 0.0,
#         "change_time": columns[8].text.strip() if len(columns) > 8 else None,
#     }
#     return stock

# def get_stock_data() -> list:
#     url = "https://www.kurzy.cz/akcie-cz/burza/"
#     html_content = fetch_page_content(url)
#     table = parse_html(html_content)
#     rows = extract_rows(table)

#     stock_data = []
#     for row in rows:
#         stock = parse_row(row)
#         if stock:
#             stock_data.append(stock)
    
#     return stock_data

# def create_stock_table(original_name: str, type_value: str, market_value: str):
#     table_name = original_name.split(',')[0].replace("akcie_", "").replace("_", " ").lower().replace(" ", "_")
#     market_value = original_name.split(',')[1].replace("_", " ").strip()

#     table = Table(
#         table_name, metadata,
#         Column('id', Integer, primary_key=True),
#         Column('date', DateTime, default=datetime.now(timezone.utc)),
#         Column('price', Float),
#         Column('volume', Integer),
#         Column('min', Float),
#         Column('max', Float),
#         Column('type', String, default=type_value),
#         Column('market', String, default=market_value),
#         extend_existing=True
#     )
#     metadata.create_all(engine)  # Create the table if it doesn't exist
#     return table

# def save_stock_data():
#     session = SessionLocal()
#     Base.metadata.create_all(bind=engine)  # Ensure the main stocks table exists
#     stock_data = get_stock_data()

#     for data in stock_data:
#         stock = Stock(
#             name=data["name"],
#             price=data["price"],
#             change=data["change"],
#             volume=data["volume"],
#             buy=data["buy"],
#             sell=data["sell"],
#             min=data["min"],
#             max=data["max"],
#             change_time=data["change_time"],
#             record_time=datetime.now(timezone.utc)
#         )
#         session.add(stock)

#         # Create a new table for the stock if it doesn't exist
#         original_name = data["name"]
#         type_value = "akcie"
#         market_value = "online burza"
#         stock_table = create_stock_table(original_name, type_value, market_value)

#         # Insert data into the stock-specific table
#         insert_statement = stock_table.insert().values(
#             date=datetime.now(timezone.utc),
#             price=data["price"],
#             volume=data["volume"],
#             min=data["min"],
#             max=data["max"],
#             type=type_value,
#             market=market_value
#         )
#         session.execute(insert_statement)
    
#     session.commit()
#     session.close()









# # ###############################################################
# # ################# spatne nazvy tabulek ########################
# # ###############################################################
# # # vytvori tabulku z kazdeho scrapu
# #                     List of relations
# #  Schema |             Name             | Type  |  Owner   
# # --------+------------------------------+-------+----------
# #  public | akcie_deutsche_bank_ag       | table | postgres
# #  public | akcie_e.on_se                | table | postgres
# #  public | akcie_e4u_a.s.               | table | postgres
# #  public | akcie_eman_a.s.              | table | postgres
# #  public | akcie_immofinanz_ag          | table | postgres
# #  public | akcie_karo_leather_a.s.      | table | postgres
# #  public | akcie_nokia                  | table | postgres
# #  public | akcie_orlen                  | table | postgres
# #  public | akcie_rbi                    | table | postgres
# #  public | akcie_rwe_ag                 | table | postgres
# #  public | akcie_tatry_mountain_resorts | table | postgres
# #  public | akcie_voestalpine_ag         | table | postgres
# #  public | akcie_volkswagen_ag          | table | postgres
# #  public | alembic_version              | table | postgres
# #  public | stocks                       | table | postgres
# # (15 rows)

# # stock_db=# SELECT * FROM akcie_deutsche_bank_ag LIMIT 1;

# #  id |            date            | price  | volume |  min   |  max  | type  |    market    | stock_type 
# # ----+----------------------------+--------+--------+--------+-------+-------+--------------+------------
# #   1 | 2024-06-28 19:08:52.364341 | 371.75 |      0 | 370.45 | 374.9 | akcie | online burza | akcie
# # (1 row)



# src/scraper.py
import os
from sqlalchemy import Table, MetaData, Column, Integer, String, Float, DateTime
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.models import Stock, Base

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

def fetch_page_content(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_html(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'class': 'pd huste leftcolumnwidth r rowcl'})
    if table is None:
        raise ValueError("Could not find the stock table on the page")
    return table

def extract_rows(table) -> list:
    return table.find_all('tr')[1:]  # Skip the header row

def parse_float(text: str) -> float:
    try:
        return float(text.replace(',', ''))
    except ValueError:
        return 0.0  # or any default value

def parse_int(text: str) -> int:
    try:
        return int(text.replace(' ', '').replace(',', ''))
    except ValueError:
        return 0  # or any default value

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
