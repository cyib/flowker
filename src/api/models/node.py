from sqlalchemy import Column, String, TEXT, DateTime, Enum, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Literal, Union

Base = declarative_base()

class GenericNode:    
    def __init__(self,
        id: str,
        name: str,
        inputsMap: list = None,
        outputsMap: list = None,
        script: str = None,
        snapshot: str = None,
        author: str = None,
        exception: str = None,
        environmentId: str = None,
        isEndpoint: bool = None,
        endpointType: str = None
    ) -> None:
        self.id = id
        self.name = name
        self.inputsMap = inputsMap
        self.outputsMap = outputsMap
        self.script = script,
        self.snapshot = snapshot,
        self.author = author
        self.exeption = exception
        self.environmentId = environmentId
        self.isEndpoint = isEndpoint
        self.endpointType = endpointType
        self.kind = None
        self.currStep = 0
        
        self.currOutputs = None
        self.firstInputs = None
        
        if script != None:
            self.kind = "Script"
        elif snapshot != None:
            self.kind = "Group"
            
        self.this = {}

class Node(Base):
    __tablename__ = 'TB_FLOWKER_NODE'

    id = Column(String(36), primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    nodeType = Column(Enum('script', 'group'))
    nodeVersion = Column(String(15), default='0.0.1')
    author = Column(String(50))
    originalNodeId = Column(String(36))
    environmentId = Column(String(36))
    isEndpoint = Column(Boolean, default=False)
    endpointType = Column(Enum('GET', 'POST'), default='GET')
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(
        self, 
        id, 
        name, 
        description=None, 
        nodeType: Literal["script", "group"] = 'script', 
        nodeVersion=None, 
        script=None,
        snapshot=None,
        originalNodeId=None,
        environmentId=None,
        isEndpoint=None,
        endpointType: Literal["GET", "POST"] = 'GET',
        createdAt=func.now(),
        updatedAt=func.now()
    ):
        self.id = id
        self.name = name
        self.description = description
        self.nodeType: Literal["script", "group"] = nodeType
        self.nodeVersion = nodeVersion
        self.script = script
        self.snapshot = snapshot
        self.originalNodeId = originalNodeId
        self.environmentId = environmentId
        self.isEndpoint = isEndpoint
        self.endpointType = endpointType
        self.createdAt = createdAt
        self.updatedAt = updatedAt