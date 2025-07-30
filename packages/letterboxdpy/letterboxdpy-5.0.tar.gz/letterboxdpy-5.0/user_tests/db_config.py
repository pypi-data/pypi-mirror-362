import os
from os.path import join
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define constants
DOTENV_FILE = join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')

# Load environment variables from .env file
load_dotenv(DOTENV_FILE)

# Create SQLAlchemy engine using the database connection string from environment variables
engine = create_engine(os.environ.get("db_conn"))

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()
