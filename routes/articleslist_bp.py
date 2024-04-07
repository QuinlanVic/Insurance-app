from flask import Blueprint, render_template, request

from models.article import Article
from extensions import db

import json

articleslist_bp = Blueprint("articleslist", __name__)

# ********* All ARTICLESLIST URLS ***********
# Defines View part of web application


# specific article page
@articleslist_bp.route("/<id>")
def article_page(id):
    specific_article = Article.query.get(id)

    if specific_article is None:
        return "<h1>Article not found</h1>"

    return render_template("article.html", article=specific_article.to_dict())


# /articleslist/add -> Add article form -> Submit -> /articleslist
@articleslist_bp.route("/add")
def add_article_page():
    return render_template("addarticle.html")


# /articleslist/update -> Update article form -> Submit -> /articleslist
# Has to be post to pass the data via body ("GET" uses URL)
# take you to update form with data after manipulation
@articleslist_bp.route("/update", methods=["POST"])
def update_article_page():
    # get the article
    article = request.form.get("article")
    # test its dtype and if it's the correct one
    print(article)
    print(type(article))
    # funny error as JSON only supports single quotes LOLOLOLOLOL
    article_json = article.replace("'", '"')
    # convert into a dict
    article_dict = json.loads(article_json)
    print(type(article_dict))
    # go to update article form
    return render_template("updatearticle.html", article=article_dict)


# ***** FORM ACTION CRUD OPERATIONS *****


# ADD article TO SQL DATABASE NOW (NOT LOCAL)
@articleslist_bp.route("/", methods=["POST"])
def new_article_list():
    # get all form data
    article_title = request.form.get("title")
    article_author = request.form.get("author")
    article_poster = request.form.get("poster")
    article_desc = request.form.get("desc")
    # create new article
    new_article = Article(
        title=article_title,
        author=article_author,
        poster=article_poster,
        desc=article_desc,
    )
    try:
        # try to add the new article
        db.session.add(new_article)
        db.session.commit()
        # get all articles
        article_list = Article.query.all()
        # convert to a list of dict
        data = [article.to_dict() for article in article_list]
        # go back to index page after adding new article
        # return render_template("index.html", articles=data)
        return f"{new_article.title} successfully created"
    except Exception as e:
        db.session.rollback()  # Undo the change (cannot be done if already committed)
        return f"<h1>An error occured: {str(e)}</h1>", 500


# UPDATE article FORM TO SQL DATABASE NOW NOT LOCAL
# has to be a different url or it will do the other "/update" above as
# it also uses a POST method because it has to for passing data via body ("GET" uses URL)
@articleslist_bp.route("/update/db", methods=["POST"])
def update_article_list():
    # get all form data
    article_id = request.form.get("id")
    article_title = request.form.get("title")
    article_author = request.form.get("author")
    article_poster = request.form.get("poster")
    article_desc = request.form.get("desc")
    # set up update data dict
    update_data = {
        "title": article_title,
        "author": article_author,
        "poster": article_poster,
        "desc": article_desc,
    }
    # get specific article to update
    specific_article = Article.query.get(article_id)
    if specific_article is None:
        return "<h1>Article not found</h1>"
    try:
        # update all values in "specific_article" with values from "update_data" dictionary
        # loop body as you only want to work with specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change it which is unsafe!!!!
            # specific_article.key = update_data.get(key, specific_article.key)
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_article, key):
                # now update those values
                setattr(specific_article, key, value)
        db.session.commit()
        # now take them to the article page
        # return f"{specific_article.title} successfully updated", render_template("article.html", article=specific_article)
        return f"{specific_article.title} successfully updated"
    except Exception as e:
        return f"<h1>An error occured: {str(e)}</h1>"


# delete article from db after pressing button
@articleslist_bp.route("/delete", methods=["POST"])
def delete_article_by_id():
    # get name from form
    id = request.form.get("article_id")
    # get the specific article
    article = Article.query.get(id)
    # test if we found the correct id value
    # print(request.form.get("article_id"))
    # article = Article.query.get(id)
    if not article:
        # return jsonify({"message": "Article not found"}), 404
        # Do not return JSON data as you want to display the information on the screen
        return "<h1>Article not found</h1>", 404
    # otherwise delete it
    try:
        db.session.delete(article)
        db.session.commit()
        # return jsonify({"message": "Article deleted successfully", "data": article.to_dict()})
        # Do not return JSON data as you want to display the information on the screen
        return f"<h1>{article.to_dict()['title']} successfully deleted</h1>"
    except Exception as e:
        # return jsonify({"error": str(e)})
        # Do not return JSON data as you want to display the information on the screen to the user
        return f"<h1>An error occured: {str(e)}</h1>", 500
