from sqlalchemy import Column, String, TEXT, DateTime, Enum, Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Literal

Base = declarative_base()

class Node(Base):
    __tablename__ = 'TB_IOFLOW_NODE'

    id = Column(String(36), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    nodeType = Column(Enum('script', 'group'))
    nodeVersion = Column(String(15), default='0.0.1')
    author = Column(String(50))
    script = Column(TEXT)
    originalNodeId = Column(String(36))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(
        self, 
        id, 
        name, 
        description=None, 
        nodeType: Literal["script", "group"] ='script', 
        nodeVersion=None, 
        script=None,
        originalNodeId=None,
        createdAt=func.now(),
        updatedAt=func.now()
    ):
        self.id = id
        self.name = name
        self.description = description
        self.nodeType: Literal["script", "group"] = nodeType
        self.nodeVersion = nodeVersion
        self.script = script
        self.originalNodeId = originalNodeId
        self.createdAt = createdAt
        self.updatedAt = updatedAt