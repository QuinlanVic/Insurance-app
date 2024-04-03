from extensions import db

import uuid


# create new Model for Article table schema
class Article(db.Model):
    __tablename__ = "articles"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    # give defaults to these values and we or authors can update them in future
    poster = db.Column(db.String(255), default="", nullable=False)
    desc = db.Column(db.String(500), default="", nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "poster": self.poster,
            "desc": self.desc,
        }
