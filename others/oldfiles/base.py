# import uuid
# from app import db

class BaseModel:
    pass
    # id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()), nullable=False)

    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()