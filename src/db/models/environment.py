from sqlalchemy import Column, String, TEXT, DateTime, Enum, Integer, func, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Environment(Base):
    __tablename__ = 'TB_FLOWKER_ENVIRONMENT'

    id = Column(String(36), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())