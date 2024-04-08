from sqlalchemy import Column, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.api.models.node import Node

Base = declarative_base()


class GenericIoMap:
    def __init__(self, name: int, type: str, required: bool = False, default: str = None):
        self.type = type
        self.name = name
        self.required = required
        self.default = default

class IoMap(Base):
    __tablename__ = 'TB_FLOWKER_IOMAP'

    id = Column(String(36), primary_key=True)
    nodeId = Column(String(36), ForeignKey(Node.id), primary_key=True)
    ioType = Column(Enum('input', 'output'))
    name = Column(String(50))
    datatype = Column(Enum('num', 'float', 'str', 'any'))
    required = Column(Boolean, default=False)
    defaultValue = Column(String(256))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    
    node = relationship(Node)
    
    def __init__(self, 
        id, 
        nodeId, 
        ioType, 
        name, 
        datatype='any', 
        required=False, 
        defaultValue=None, 
        createdAt=func.now(), 
        updatedAt=func.now()
    ):
        self.id = id
        self.nodeId = nodeId
        self.ioType = ioType
        self.name = name
        self.datatype = datatype
        self.required = required
        self.defaultValue = defaultValue
        self.createdAt = createdAt
        self.updatedAt = updatedAt