# src/initialize_db.py
from dotenv import load_dotenv
import os

load_dotenv()

# Postgres environment variables
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Create database
os.system(f"docker exec -i postgres createdb -U {POSTGRES_USER} {POSTGRES_DB}")
