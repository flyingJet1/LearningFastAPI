from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from .config import settings

uri = urllib.parse.quote_plus(f"DRIVER={settings.database_driver};SERVER={settings.database_hostname};DATABASE={settings.database_name};UID={settings.database_username};PWD={settings.database_password}")
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % uri)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

