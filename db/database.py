from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL="postgresql://root:root@localhost/northwind"

engine = create_engine(DATABASE_URL)
sessionmaker(bind=engine)