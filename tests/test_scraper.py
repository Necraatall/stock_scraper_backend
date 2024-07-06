# tests/test_scraper.py
from src.scraper import fetch_page_content, parse_stock_table, extract_rows, extract_data_from_row, extract_stock_data

def test_fetch_page_content():
    url = "https://www.kurzy.cz/akcie-cz/burza/bcpp_online"
    html_content = fetch_page_content(url)
    assert html_content is not None
    assert len(html_content) > 0

def test_parse_stock_table():
    url = "https://www.kurzy.cz/akcie-cz/burza/bcpp_online"
    html_content = fetch_page_content(url)
    table = parse_stock_table(html_content)
    assert table is not None

def test_extract_rows():
    url = "https://www.kurzy.cz/akcie-cz/burza/bcpp_online"
    html_content = fetch_page_content(url)
    table = parse_stock_table(html_content)
    rows = extract_rows(table)
    assert len(rows) > 0

def test_extract_data_from_row():
    url = "https://www.kurzy.cz/akcie-cz/burza/bcpp_online"
    html_content = fetch_page_content(url)
    table = parse_stock_table(html_content)
    rows = extract_rows(table)
    row_data = extract_data_from_row(rows[0])
    assert 'name' in row_data
    assert 'price' in row_data
    assert 'change' in row_data
    assert 'volume' in row_data
    assert 'buy' in row_data
    assert 'sell' in row_data
    assert 'min' in row_data
    assert 'max' in row_data
    assert 'time' in row_data or row_data['time'] is None

def test_extract_stock_data():
    url = "https://www.kurzy.cz/akcie-cz/burza/bcpp_online"
    html_content = fetch_page_content(url)
    table = parse_stock_table(html_content)
    stock_data_list = extract_stock_data(table)
    assert len(stock_data_list) > 0
    for stock_data in stock_data_list:
        assert 'name' in stock_data
        assert 'price' in stock_data
        assert 'change' in stock_data
        assert 'volume' in stock_data
        assert 'buy' in stock_data
        assert 'sell' in stock_data
        assert 'min' in stock_data
        assert 'max' in stock_data
        assert 'time' in stock_data or stock_data['time'] is None
