from extensions import db

import uuid

from flask_login import UserMixin


# create new Model for User table schema
# "UserMixin" ensures that the User class comes with all the default methods
class UserClaim(UserMixin, db.Model):
    __tablename__ = "usersclaims"
    # automatically creates and assigns value
    claim_id = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id = db.Column(db.String(50), db.ForeignKey("User.id"))
    amount = db.Column(db.Float(100), nullable=False)
    desc = db.Column(db.String(500), default="", nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "claim_id": self.claim_id,
            "amount": self.amount,
            "desc": self.desc,
        }
