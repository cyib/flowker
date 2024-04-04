from sqlalchemy import Column, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class IoMap(Base):
    __tablename__ = 'TB_IOFLOW_IOMAP'

    id = Column(String(36), primary_key=True)
    nodeId = Column(String(36), ForeignKey('TB_IOFLOW_NODE.id'), primary_key=True)
    ioType = Column(Enum('input', 'output'))
    name = Column(String(50))
    datatype = Column(Enum('num', 'float', 'str', 'any'))
    required = Column(Boolean, default=False)
    defaultValue = Column(String(256))
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())