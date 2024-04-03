import uuid
# from app import db
from .base import BaseModel

class ApcModel(BaseModel):
    pass
    # __tablename__ = 'apcs'

    # # Defina seus campos de modelo aqui
    # id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    # name = db.Column(db.String(50), nullable=False)
    # inputs = db.Column(db.Text, nullable=True)
    # outputs = db.Column(db.Text, nullable=True)
    # script = db.Column(db.Text, nullable=True)
    # # ...

    # def __init__(self, id, name, inputs, outputs, script):
    #     self.id = id
    #     self.name = name
    #     self.inputs = inputs
    #     self.outputs = outputs
    #     self.script = script

    # def __repr__(self):
    #     return f'<Apc {self.name}>'