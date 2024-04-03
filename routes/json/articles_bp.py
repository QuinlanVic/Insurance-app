from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from app import Article, db

# ********** THESE ARE FOR JSON REQUESTS BY FRONT-END DEVELOPERS **********

# or no import and this code
# class Article(db.Model):
#     __tablename__ = "articles"
#     # automatically creates and assigns value
#     id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
#     title = db.Column(db.String(100), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     # give defaults to these values and we or authors can update them in future
#     poster = db.Column(db.String(255), default="")
#     desc = db.Column(db.String(500), default="")

#     # JSON - Keys (can change names sent to front-end)
#     # class method
#     # dict is also easier to convert to JSON
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "author": self.author,
#             "poster": self.poster,
#             "desc": self.desc,
#         }
# db = SQLALchemy()

# create new instance of Blueprint class called "articles"
articles_bp = Blueprint("articles", __name__)


# ONLY JSON REQUESTS TO DATABASE


# Get all articles from azure request
@articles_bp.get("/")
def get_articles():
    article_list = Article.query.all()  # SELECT * FROM articles | article_list iterator
    data = [article.to_dict() for article in article_list]  # convert to a list of dict
    # print(data)
    # print(type(jsonify(data)))
    # return jsonify(data)
    return data


# Get a specific article from azure request
@articles_bp.get("/<id>")
def get_specific_article(id):
    # print(type(id))  # string

    # get specific article
    specific_article = Article.query.get(id)

    if specific_article is None:
        result = {"message": "article not found"}
        return jsonify(result), 404

    # convert to a dictionary to put in JSON
    data = specific_article.to_dict()
    result = {"message": "article successfully found", "data": data}
    return jsonify(result)


# Create a new article and add it to azure db request
@articles_bp.post("/")
def create_article():
    # get new article JSON data from body in request
    data = request.json
    # create a new article with it, no id as it is automatically created and assigned
    new_article = Article(
        title=data["title"],
        author=data["author"],
        poster=data["poster"],
        desc=data["desc"],
    )
    # if keys of Model and keys of data sent from users side are the same then you can use unpacking
    # risk = if they provide an "id" value, it is added (not automatically generated)
    # new_article = article(**data)
    try:
        db.session.add(new_article)
        db.session.commit()
        # check if article is correctly updated
        print(new_article)
        # create message to return
        result = {
            "message": "article added successfully",
            "data": new_article.to_dict(),
        }
        # added status code
        return jsonify(result), 201
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured": str(e)}
        return jsonify(result), 500


# Update specific article and add to azure db request
@articles_bp.put("/<id>")
def update_article(id):
    # get data from request body
    update_data = request.json
    # get specific article
    specific_article = Article.query.get(id)
    # if not found
    if specific_article is None:
        result = {"message": "article not found"}
        return jsonify(result), 404
    try:
        # update all values in "specific_article" with values from "update_data" dictionary
        # loop request body data (update_data) as you only want to work with the specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change our db which is unsafe!!!!
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_article, key):
                # update the value of that key
                setattr(specific_article, key, value)
                # commit changes after all keys have been updated
        db.session.commit()
        # check if article was correctly updated
        # print(specific_article)
        result = {
            "messsage": "article successfully updated",
            "data": specific_article.to_dict(),
        }
        return jsonify(result)
    # if an error occured while updating
    except Exception as e:
        db.session.rollback()  # undo the changes (unless they have already been committed)
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500


# Delete the specific article from azure db request
@articles_bp.delete("/<id>")
def delete_article(id):
    # get specific article from "id" in URL
    article_del = Article.query.get(id)
    # if we did not find it
    if not article_del:
        result = {"message": "article not found"}
        return jsonify(result), 404
    try:
        # delete from database
        db.session.delete(article_del)
        # making the change permanent
        db.session.commit()
        result = {
            "messsage": "article successfully deleted",
            "data": article_del.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500
