from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL="postgresql+psycopg://postgres:root@localhost/Northwind"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def getSession():
    return SessionLocal()