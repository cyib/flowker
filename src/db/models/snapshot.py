from sqlalchemy import Column, String, TEXT, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Snapshot(Base):
    __tablename__ = 'TB_IOFLOW_SNAPSHOT'

    id = Column(String(36), primary_key=True)
    nodeId = Column(String(36), ForeignKey('TB_IOFLOW_NODE.id'))
    snapshot = Column(TEXT)