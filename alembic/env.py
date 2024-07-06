# alembic/env.py
import os
from src.models import Base
from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the Alembic configuration file
config = context.config

# Configure logging from the config file
fileConfig(config.config_file_name)

# Set the target metadata for autogeneration
target_metadata = Base.metadata

# Get the URL from the environment variables
DATABASE_URL = os.getenv('DATABASE_URL')
ALEMBIC_URL = os.getenv('ALEMBIC_URL')

# Function to create the engine with pool_pre_ping
def get_engine():
    return create_engine(
        ALEMBIC_URL,
        pool_pre_ping=True,
    )

# Function for running migrations in offline mode
def run_migrations_offline():
    """Run migrations in offline mode."""
    context.configure(
        url=ALEMBIC_URL, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Function for running migrations in online mode
def run_migrations_online():
    """Run migrations in online mode."""
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
