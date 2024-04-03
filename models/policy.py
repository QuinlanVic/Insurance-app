from extensions import db

import uuid


# schema for the policies table
class Policy(db.Model):
    __tablename__ = "policies"
    # automatically creates and assigns value
    # increased performance if you do not do calculations to update id by max id on the python side
    # if autoincremented on the SQL side it will not have a decrease in preformance as it will remember the last value and update easily
    # increased security as it is more difficult for people to guess "id" values
    # easier to merge two tables as their id primary keys will not be the same/consist of duplicates
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(50), nullable=False)
    # give defaults to these values as we or users can update them in future
    poster = db.Column(db.String(255), default="", nullable=False)
    desc = db.Column(db.String(500), default="", nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "poster": self.poster,
            "desc": self.desc,
        }
