from extensions import db

import uuid

from flask_login import UserMixin


# create new Model for User table schema
# "UserMixin" ensures that the User class comes with all the default methods
class User(UserMixin, db.Model):
    __tablename__ = "users"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    # make unique
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # give defaults to these values and we or users can update them in future
    pic = db.Column(db.String(255), default="", nullable=False)
    # get rid of this and use "userpolicies" table
    # policy_id = db.Column(db.String(200), default="0", nullable=False)

    # What does db.relationship() do? That function returns a new property that can do multiple things.
    # In this case we told it to point to the Address class and load multiple of those.
    # How does it know that this will return more than one address? Because SQLAlchemy guesses a useful default from your declaration.
    # If you would want to have a one-to-one relationship you can pass uselist=False to relationship().
    # one-to-many relationships with other tables
    mypolicies = db.relationship("UserPolicy", backref="user", lazy=True)
    claimsmade = db.relationship("UserClaim", backref="user", lazy=True)

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
        }


class UserPolicy(db.Model):
    __tablename__ = "userspolicies"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    # name of table in class
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    policy_id = db.Column(db.String(50), db.ForeignKey("policies.id"), nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "policy_id": self.policy_id,
        }


class Claim(db.Model):
    __tablename__ = "claims"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float(), nullable=False)
    desc = db.Column(db.String(500), default="", nullable=False)
    claim_maker = db.relationship("UserClaim", backref="claim", lazy=True)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "desc": self.desc,
        }


class UserClaim(db.Model):
    __tablename__ = "usersclaims"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = db.Column(db.String(50), db.ForeignKey("claims.id"))
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"))

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "claim_id": self.claim_id,
            "user_id": self.user_id,
        }
