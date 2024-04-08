from sqlalchemy import Column, String, TEXT, DateTime, Enum, Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Literal, Union

Base = declarative_base()

class GenericEnvironment:    
    def __init__(self,
        id: str,
        name: str,
        description: str = None,
        color: str = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.color = color
        
class Environment(Base):
    __tablename__ = 'TB_FLOWKER_ENVIRONMENT'

    id = Column(String(36), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    color = Column(String(16))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(
        self, 
        id, 
        name, 
        description=None, 
        color=None,
        createdAt=func.now(),
        updatedAt=func.now()
    ):
        self.id = id
        self.name = name
        self.description = description
        self.color = color
        self.createdAt = createdAt
        self.updatedAt = updatedAt