# blueprint for miscallaneous routes/pages
from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required

from flask_wtf import FlaskForm
from extensions import db

from models.article import Article
from models.employee import Employee

main_bp = Blueprint("main", __name__)


# from + import combo to only import what we need to improve performance
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    EmailField,
    IntegerField,
    DecimalField,
)
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange

from flask_login import login_user, logout_user, login_required

from datetime import datetime


# signup validation
class QuoteForm(FlaskForm):
    year = IntegerField("year", validators=[InputRequired()])
    price = DecimalField("price", validators=[InputRequired()])
    submit = SubmitField("Calculate Quote")


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


# define a route for /getquote page
@main_bp.route("/getquote", methods=["GET", "POST"])
def get_quote_page():
    form = QuoteForm()
    # only on POST (when user is logging in)
    if form.validate_on_submit():

        # go back to quote page
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return abort(400)
        cover = 50000
        premium = 500
        flash(
            "We can offer you R"
            + f"{cover}"
            + " in cover and you would pay R"
            + f"{premium}"
            + " per month :)"
        )
        return render_template("getquote.html", form=form)
    # Only on GET - use form instance in "getquote" page
    return render_template("getquote.html", form=form)
