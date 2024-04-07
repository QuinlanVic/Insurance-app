from extensions import db

import uuid

from flask_login import UserMixin


# create new Model for User table schema
class User(UserMixin, db.Model):
    __tablename__ = "users"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    # make unique
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # give defaults to these values and we or users can update them in future
    pic = db.Column(db.String(255), default="", nullable=False)
    policy_id = db.Column(db.String(50), default="0", nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "pic": self.pic,
            "policy_id": self.policy_id,
        }