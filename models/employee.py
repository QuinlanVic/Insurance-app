from extensions import db

import uuid


# create new Model for Employee table schema
class Employee(db.Model):
    __tablename__ = "employees"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    # give defaults to these values as we or users can update them in future
    pic = db.Column(db.String(255), default="", nullable=False)
    desc = db.Column(db.String(500), default="", nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "job_title": self.job_title,
            "pic": self.pic,
            "desc": self.desc,
        }
