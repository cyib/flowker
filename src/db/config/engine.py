from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from src.env.environment import FLOWKER_DATABASE_COMPLETE_PATH

engine = create_engine(f'sqlite:///{FLOWKER_DATABASE_COMPLETE_PATH}')

def create_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()
