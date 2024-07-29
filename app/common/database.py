"""Set up the connection into the database"""

import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

db_user = os.environ["DB_USER"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]
db_pwd = os.environ["DB_PASSWORD"]
db_port = os.environ["DB_PORT"]
DATABASE_URL = f"postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)
new_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_new_session() -> Generator[Session]:
    session = new_session()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()
