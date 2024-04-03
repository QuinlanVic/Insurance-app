# blueprint for miscallaneous routes/pages
from flask import Blueprint, render_template
from flask_login import login_required

from models.article import Article
from models.employee import Employee

main_bp = Blueprint("main", __name__)


# testing route for formatting/developing header and footer in "base.html"
@main_bp.route("/base")
def base_page():
    return render_template("base.html")


# root URL
# index page with articles
@main_bp.route("/")  # HOF
def index_page():
    article_list = Article.query.all()  # SELECT * FROM articles | article_list iterator
    # print(type(article_list)) # list
    # print(type(article_list[0])) # main_bp.article
    data = [article.to_dict() for article in article_list]  # convert to a list of dict
    return render_template("index.html", articles=data)


# Define a route for the /aboutus URL
@main_bp.route("/aboutus")
def about_page():
    # get all employees to display them on the screen
    employees = Employee.query.all()
    return render_template("aboutus.html", employees=employees)
    # testing issue
    # return render_template("aboutus.html")


# Define a route for the /help page
@main_bp.route("/help")
def help_page():
    # do not need to get any data from the server
    return render_template("help.html")
