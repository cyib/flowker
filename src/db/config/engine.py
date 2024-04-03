import logging
from sqlalchemy import create_engine, Transaction
from sqlalchemy.orm import sessionmaker
from .environment import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from sqlalchemy.orm.session import Session

connect_args = {
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,
    'database': DB_NAME,
    'port': DB_PORT
}

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine('mysql+mysqlconnector://', connect_args=connect_args)

def create_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()