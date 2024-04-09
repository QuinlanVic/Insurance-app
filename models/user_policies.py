from extensions import db

import uuid

from flask_login import UserMixin


# create new Model for User table schema
# "UserMixin" ensures that the User class comes with all the default methods
class UserPolicy(UserMixin, db.Model):
    __tablename__ = "userspolicies"
    # automatically creates and assigns value
    user_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    policy_id = db.Column(db.String(200), default="0", nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "policy_id": self.policy_id,
        }
