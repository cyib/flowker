from sqlalchemy import Column, String, TEXT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.api.models.node import Node

Base = declarative_base()

class Snapshot(Base):
    __tablename__ = 'TB_IOFLOW_SNAPSHOT'

    id = Column(String(36), primary_key=True)
    nodeId = Column(String(36), ForeignKey(Node.id))
    snapshot = Column(TEXT)
    
    def __init__(self, id, nodeId, snapshot):
        self.id = id
        self.nodeId = nodeId
        self.snapshot = snapshot