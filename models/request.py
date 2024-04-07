from extensions import db

import uuid


# create new Model for Request table schema
class Request(db.Model):
    __tablename__ = "requests"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    phone_num = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    msg = db.Column(db.String(500), nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_num": self.phone_num,
            "email": self.email,
            "msg": self.msg,
        }
