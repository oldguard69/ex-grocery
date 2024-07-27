"""
Set up the connection into the database
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db_user = os.environ["DB_USER"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]
db_pwd = os.environ["DB_PASSWORD"]
DATABASE_URL = f"postgresql://{db_user}:{db_pwd}@{db_host}/{db_name}"
print("database url", DATABASE_URL)

engine = create_engine(DATABASE_URL)
new_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
