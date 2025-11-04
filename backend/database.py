from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

from .models import Base

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    print("INFO: Attempting to connect to DB and create tables if they do not exist...")
    Base.metadata.create_all(bind=engine)
    print("INFO: Database initialization complete.")

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
