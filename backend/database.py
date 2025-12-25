from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
db_pass = os.getenv("DATABASE_PASSWORD")
db_user = os.getenv("DATABASE_USER")
db_name = os.getenv("DATABASE_NAME")
db_host = os.getenv("DATABASE_HOST")
db_port = os.getenv("DATABASE_PORT")
DB_URL = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
engine = create_engine(DB_URL,echo = True)
SessionLocal = sessionmaker(bind = engine, autocommit= False, autoflush = False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()