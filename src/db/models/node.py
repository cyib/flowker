from sqlalchemy import Column, String, TEXT, DateTime, Enum, Integer, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Node(Base):
    __tablename__ = 'TB_IOFLOW_NODE'

    id = Column(String(36), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    nodeType = Column(Enum('script', 'group'))
    nodeVersion = Column(Integer)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())