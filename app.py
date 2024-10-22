from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import os
from dotenv import load_dotenv

from extensions import db

from models.user import User

from flask_login import LoginManager

login_manager = LoginManager()

import pymysql
pymysql.install_as_MySQLdb()


# CONNECT TO MSSM Database
# All to keep away private passwords and stuff away from the public via
# puts variables in .env file into windows environmental variables
load_dotenv()  # load -> os env (environmental variables)
# print(os.environ.get("AZURE_DATABASE_URL"))


# Create a instance of Flask
app = Flask(__name__)

# secret so we have to provide it in the ".env" file
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY3")  # CSRF token


# General Pattern
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

# connect to our local server and db
# change connection string when working with different databases
connection_string = os.environ.get("LOCAL_DATABASE_URL2")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

db.init_app(app)
# Sqlalchemy is a Python SQL toolkit & ORM ->
# easy to submit SQL queries as well as map objects to table definitions and vice versa
# db = SQLAlchemy(app)  # ORM
# 3 advantages of working with the ORM
# convert to raw sql query
# can read from/work with multiple databases (just change connection string)
# no raw sql -> autocomplete functions, E.g. NOT ("SELECT * policies...") in string format
# allows us to manipulate easier to work with datatypes such as lists of dicts (NOT query strings like above)
# pyodbc = driver to connect to database

login_manager.init_app(app)


# ***** MISCELLANEOUS ROUTES *****
from routes.main_bp import main_bp

# registering "main_bp.py" as a blueprint
app.register_blueprint(main_bp)

# ***** POLICIES *****
# have to have import blueprints here because by now the db would have been created and
# all blueprints can import db from app without circular dependencies
from routes.json.policies_bp import policies_bp

# registering "policies_bp.py" as a blueprint and add a prefix for the url
# JSON (For front-end people)
app.register_blueprint(policies_bp, url_prefix="/policies")

# ***** POLICIESLIST *****
from routes.policieslist_bp import policieslist_bp

# registering "policieslist_bp.py" as a blueprint and add a prefix for the url
# view (Python fullstack) -> actually implementing through forms and stuff
app.register_blueprint(policieslist_bp, url_prefix="/policieslist")

# ***** EMPLOYEES *****
from routes.json.employees_bp import employees_bp

# registering "employees_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(employees_bp, url_prefix="/employees")

# ***** USERS *****
from routes.json.users_bp import users_bp


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# registering "users_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(users_bp, url_prefix="/users")

# ***** ARTICLES *****
from routes.json.articles_bp import articles_bp

# registering "articles_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(articles_bp, url_prefix="/articles")

# ***** ARTICLESLIST *****
from routes.articleslist_bp import articleslist_bp

# registering "articleslist_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(articleslist_bp, url_prefix="/articleslist")

# ***** ARTICLESLIST *****
from routes.profile_bp import profile_bp

# registering "articleslist_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(profile_bp, url_prefix="/profile")

# ***** LOGINANDSIGNUP *****
from routes.user_bp import user_bp

# registering "user_bp.py" as a blueprint
app.register_blueprint(user_bp)


# to test connection
try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # only use "create_all" once and then comment out again
        # so it doesn't try to create tables with each restart of the server
        # it won't cause an error as it only adds if the table doesn't exist
        # but always keep "create_all" when in production (for updates)
        # delete and then recreate tables
        # db.drop_all()
        # db.create_all()  # easier way to create tables through python after connecting
except Exception as e:
    print("Error connecting to the database:", e)
