from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./hotel.db"  # SQLite for simplicity
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
