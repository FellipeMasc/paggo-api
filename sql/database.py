from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL


# connection_url = URL.create(
#     "mssql+pyodbc",
#     username="sa",
#     password="12345678",
#     host="10.255.255.254",
#     database="paggo",
#     query={
#         "driver": "ODBC Driver 17 for SQL Server",
#         "TrustServerCertificate": "yes"
#     },
# )

engine = create_engine('sqlite:///./sql/paggo.sqlite3', echo=True)



conn = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()