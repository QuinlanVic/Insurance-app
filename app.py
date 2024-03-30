from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import os
from dotenv import load_dotenv
import uuid

from flask_wtf import FlaskForm

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

# connect to our azure server and db
# change connection string when working with different databases
connection_string = os.environ.get("AZURE_DATABASE_URL2")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
# Sqlalchemy is a Python SQL toolkit & ORM ->
# easy to submit SQL queries as well as map objects to table definitions and vice versa
db = SQLAlchemy(app)  # ORM
# 3 advantages of working with the ORM driver
# can read from/work with multiple databases (just change connection string)
# no raw sql -> autocomplete functions, E.g. NOT ("SELECT * policies...") in string format
# allows us to manipulate easier to work with datatypes such as lists of dicts (NOT query strings like above)


# connect to our azure and create table(s)
# constructor we are using is from "db.Model"
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
    poster = db.Column(db.String(255), default="")
    desc = db.Column(db.String(500), default="")

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


# create new Model for Employee table schema
class Employee(db.Model):
    __tablename__ = "employees"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    # give defaults to these values as we or users can update them in future
    pic = db.Column(db.String(255), default="")
    desc = db.Column(db.String(500), default="")

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


# create new Model for User table schema
class User(db.Model):
    __tablename__ = "users"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    # make unique
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # give defaults to these values and we or users can update them in future
    pic = db.Column(db.String(255), default="")
    policy_id = db.Column(db.String(50), default="0")

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "pic": self.pic,
            "policy_id": self.policy_id,
        }


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
        db.create_all()  # easier way to create tables through python after connecting
except Exception as e:
    print("Error connecting to the database:", e)

# ***** POLICIES *****
# have to have import blueprints here because by now the db would have been created and
# all blueprints can import db from app without circular dependencies
from policies_bp import policies_bp

# registering "policies_bp.py" as a blueprint and add a prefix for the url
# JSON (For front-end people)
app.register_blueprint(policies_bp, url_prefix="/policies")

# ***** POLICIESLIST *****
from policieslist_bp import policieslist_bp

# registering "policieslist_bp.py" as a blueprint and add a prefix for the url
# view (Python fullstack) -> actually implementing through forms and stuff
app.register_blueprint(policieslist_bp, url_prefix="/policieslist")

# ***** EMPLOYEES *****
from employees_bp import employees_bp

# registering "employees_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(employees_bp, url_prefix="/employees")

# ***** USERS *****
from users_bp import users_bp

# registering "users_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(users_bp, url_prefix="/users")


# testing route for formatting/developing header and footer in "base.html"
@app.route("/base")
def base_page():
    return render_template("base.html")


# root URL
@app.route("/")  # HOF
def home_page():
    return render_template("index.html")


# Define a route for the /about URL
@app.route("/about")
def about_page():
    return render_template("about.html", employees=employees)


# Define a route for the /help page
@app.route("/help")
def help_page():
    return render_template("help.html")


# from + import combo to only import what we need to improve performance
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError


# signup validation
class SignUpForm(FlaskForm):
    name = StringField("name", validators=[InputRequired(), Length(min=6)])
    email = EmailField("email", validators=[InputRequired()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    # use WTF to send user back to signup page if input is invalid
    # automatically runs when the "form.validate_on_submit()" function executes
    # class method (instance and data from user form via field)
    # validate_<field name>
    def validate_email(self, field):
        # inform WTF that there is an error and display it
        print("Validate email was called (reg)", field.data)
        # check if there is an existing email
        specific_user = User.query.filter_by(email=field.data).first()
        # print(specific_user)

        # if it does exist then user cannot sign up and send them back to register page
        if specific_user:
            # the message below is displayed in the "div" in the register form
            raise ValidationError("Email already exists")


# login validation
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

    def validate_email(self, field):
        # inform WTF that there is an error and display it
        print("Validate email was called (log)", field.data)
        # check if email exists
        specific_user = User.query.filter_by(email=field.data).first()
        # print(specific_user)

        # if it does not exist then user cannot log in and we send them back to login page
        if not specific_user:
            # the message below is displayed in the "div" in the register form
            raise ValidationError("Email or password invalid")

    # Validate for login form
    def validate_password(self, field):
        # access email via self
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if user.password != field.data:
                raise ValidationError("Email or password is invalid")


# Define a route for the /profile page
@app.route("/profile/<id>")
def profile_page(id):
    profile = User.query.get(id)
    return render_template("profile.html", profile=profile)


# GET - Issue token
# POST - Verify token
# new route for login page
# Define a route for the login page
@app.route("/login", methods=["GET", "POST"])  # HOF
def login_page():
    # create a new form object
    form = LoginForm()

    # only on POST (when user is logging in)
    if form.validate_on_submit():
        # check if email is already in database
        specific_user = User.query.filter_by(email=form.email.data).first()
        print(specific_user)

        # if it does not exist or the password is incorrect
        # then user cannot login and send them back to login page
        if not specific_user or specific_user.password != form.password.data:
            return render_template("login.html", form=form)
        # otherwise user has logged in successfully
        return f"<h1>Welcome back, {specific_user.name}"

    # only on GET
    # use "form" in login page
    return render_template("login.html", form=form)


# GET - Issue token
# POST - Verify token
# new route for register page
@app.route("/signup", methods=["GET", "POST"])  # HOF
def signup_page():
    # GET & POST
    # create a new form object
    form = SignUpForm()

    # only on POST (when user is signing up)
    if form.validate_on_submit():
        # check if email is already in database
        specific_user = User.query.filter_by(email=form.email.data).first()
        print(specific_user)

        # if it does exist then user cannot sign up and send them back to signup page
        if specific_user:
            return render_template("signup.html", form=form)
        # otherwise create a new user entry
        # print(form.email.data, form.password.data)
        # add registered users to the database
        new_user = User(
            name=form.name.data, email=form.email.data, password=form.password.data
        )  # id should be auto-created alongside pic and policy-id
        try:
            db.session.add(new_user)
            db.session.commit()
            # print("Profile page", name, email, password)
            return "<h1> Registration successful </h1>", 201
        # now send them to new profile page
        # return render_template("profile.html", new_user.to_dict())
        except Exception as e:
            db.session.rollback()  # undo the change (unless committed already)
            return f"<h1>An error occured: {str(e)}", 500

    # only on GET
    # then use "form" in signup page
    return render_template("signup.html", form=form)


# go to homepage when posting from login page
@app.route("/", methods=["POST"])
def go_to_index():
    # have to get values from form via keys
    email = request.form.get("email")
    password = request.form.get("password")
    print("Profile page", email, password)
    return "<h1>Welcome back</h1>", render_template("index.html")


# go to profile page when posting from signup page
@app.route("/profile", methods=["POST"])
def go_to_profile():
    # have to get values from form via keys
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    # have to create a new user and add them to user list
    new_user = {
        "name": name,
        "email": email,
        password: "password",
        "pic": "",
        "policy-id": 0,
    }

    user_ids = [user["id"] for user in users]
    # print(user_ids) # check if you have got all the ids successfully
    max_id = max(user_ids)
    # print(max_id) # check if you have max id sucessfully
    new_user["id"] = max_id + 1
    # print(new_user) # check if new user has been crafted successfully

    # add to users list of dict
    users.append(new_user)
    print("Profile page", email, password)
    return render_template("profile.html", user=new_user)


# store tokens in browser (local storage or cookies) (gets given after signing up/logging in)
# no token, no data
