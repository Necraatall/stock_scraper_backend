from logging.config import fileConfig
import os
from sqlalchemy import create_engine
from alembic import context
from dotenv import load_dotenv

# Načtení proměnných prostředí z .env souboru
load_dotenv()

# Tento import závisí na tom, kde máte definovaný váš Base objekt
from src.models import Base

# Načtení config souboru
config = context.config

# Konfigurace logování z config souboru
fileConfig(config.config_file_name)

# Nastavení target_metadata pro autogenerování
target_metadata = Base.metadata

# Získání URL z prostředí
DATABASE_URL = os.getenv('DATABASE_URL')
ALEMBIC_URL = os.getenv('ALEMBIC_URL')

# Funkce pro vytvoření engine s pool_pre_ping
def get_engine():
    return create_engine(
        ALEMBIC_URL,
        pool_pre_ping=True,
    )

# Funkce pro offline migrace
def run_migrations_offline():
    """Spustí migrace v offline módu."""
    context.configure(
        url=ALEMBIC_URL, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Funkce pro online migrace
def run_migrations_online():
    """Spustí migrace v online módu."""
    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
