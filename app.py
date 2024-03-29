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
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY2")  # CSRF token


# General Pattern
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

# connect to our azure server and db
# change connection string when working with different databases
connection_string = os.environ.get("AZURE_DATABASE_URL")
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


# some dummy employee data
employees = [
    {
        "id": 1,
        "name": "Paul Flex",
        "job-title": "CEO",
        "pic": "https://t4.ftcdn.net/jpg/06/35/15/47/360_F_635154757_zU5ZxxZe3Vs0hrrOQ9WBgNgX8s4Cw19s.jpg",
        "desc": "Paul Flex is CoolWater's Chief Executive Officer",
    },
    {
        "id": 2,
        "name": "Sarah Blue",
        "job-title": "CFO",
        "pic": "https://t4.ftcdn.net/jpg/06/12/73/89/360_F_612738927_LIcFCiKHQhHq9R1QhkVRKvT6RelYUmgv.jpg",
        "desc": "Sarah Bleu is CoolWater's Chief Financial Officer",
    },
    {
        "id": 3,
        "name": "Mandla Ngcobo",
        "job-title": "CHRO",
        "pic": "https://www.goodthingsguy.com/wp-content/uploads/2020/07/vusi-thembekwayo-biography-age-net-worth-wife-2.jpg",
        "desc": "Mandla Ngcobo is Coolwater's Chief Human Resources Officer",
    },
]

# some dummy policy data
policies = [
    {
        "id": 1,
        "name": "Blue Car Insurance",
        "price": 500,
        "poster": "https://c4.wallpaperflare.com/wallpaper/14/17/129/2011-hyundai-i10-wallpaper-preview.jpg",
        "desc": "Blue Car Insurance is affordable and is targeted at students and young professionals",
    },
    {
        "id": 2,
        "name": "Cool Car Insurance",
        "price": 1000,
        "poster": "https://c4.wallpaperflare.com/wallpaper/373/463/605/volkswagen-rain-gti-hd-silver-coupe-wallpaper-preview.jpg",
        "desc": "Cool Car Insurance is targeted at established professionals and middle aged individuals",
    },
    {
        "id": 3,
        "name": "Water Car Insurance",
        "price": 1500,
        "poster": "https://moewalls.com/wp-content/uploads/2024/01/bmw-m4-rainy-night-thumb.jpg",
        "desc": "Water Car Insurance is targeted at small families",
    },
    {
        "id": 4,
        "name": "CoolWater Car Insurance",
        "price": 2000,
        "poster": "https://c4.wallpaperflare.com/wallpaper/634/597/281/luxury-suv-range-rover-velar-2017-4k-wallpaper-preview.jpg",
        "desc": "CoolWater is targeted at medium to large families",
    },
    {
        "id": 5,
        "name": "CoolCool Car Insurance",
        "price": 2500,
        "poster": "https://c4.wallpaperflare.com/wallpaper/131/207/698/forest-rain-forest-ford-wallpaper-preview.jpg",
        "desc": "CoolCool Car Insurance is targeted at those with antique vehicles",
    },
    {
        "id": 6,
        "name": "WaterCool Car Insurance",
        "price": 3000,
        "poster": "https://i.pinimg.com/originals/56/c3/74/56c3744dc273cab7d050b9943d2accfa.jpg",
        "desc": "WaterCool Car Insurance is targeted at those with sports cars",
    },
]

# some dummy user data
users = [
    {
        "id": 1,
        "name": "Ethan Rich",
        "email": "E.rich@gmail.com",
        "pic": "",
        "policy-id": 0,
    },
    {
        "id": 2,
        "name": "Scarlet Ndlovu",
        "email": "Scar.let@gmail.com",
        "pic": "",
        "policy-id": 1,
    },
    {
        "id": 3,
        "name": "Bertha Pudding",
        "email": "Bertha@gmail.com",
        "pic": "",
        "policy-id": 4,
    },
]


# root URL
@app.route("/")
def home_page():
    return render_template("index.html")


# policies page
@app.route("/policies")
def policies_page():
    # policies = json.loads(get_policies())
    return render_template("policies.html", policies=policies)


# one policy entry to test what policy page displays
policylocal = {
    "id": 1,
    "name": "Blue Car Insurance",
    "price": 500,
    "poster": "https://c4.wallpaperflare.com/wallpaper/14/17/129/2011-hyundai-i10-wallpaper-preview.jpg",
    "desc": "Blue Car Insurance is affordable and is targeted at students and young professionals",
}


# policy page
@app.route("/policies/<id>")
def policy_page(id):
    # policy = get_policy(id)
    # print(type(policy))
    # search through policies list and find the policy with the specified id (None (default value) if not found)
    print(id)
    specific_policy = next(
        (policy for policy in policies if policy["id"] == int(id)), None
    )
    # if policy is not found
    if specific_policy is None:
        # result = {"message": "policy not found"}
        # return a not found message and appropriate status code (json)
        return "<h1>Error: Policy not found :(</h1>"
    # otherwise policy has been found so we return a success message and the policy data (json)
    # result = {"message": "policy successfully found", "data": specific_policy}
    # return jsonify(result)
    return render_template("policy.html", policy=specific_policy)


# Define a route for the /about URL
@app.route("/about")
def about_page():
    return render_template("about.html", employees=employees)


# Define a route for the /help page
@app.route("/help")
def help_page():
    return render_template("help.html")


# Define a route for the /profile page
@app.route("/profile/<id>")
def profile_page(id):
    profile = get_user(id)
    return render_template("profile.html", profile=profile)


# testing route for formatting/developing header and footer in "base.html"
@app.route("/base")
def base_page():
    return render_template("base.html")


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


# ************ CRUD OPERATIONS FOR USER *********************************************************************************************
# GET -> all users -> JSON
@app.get("/users")
def get_users():
    # have to convert to JSON (using jsonify library from Flask)
    return jsonify(users)


# GET -> specific user -> JSON
@app.get("/users/<id>")
def get_user(id):
    # search through users list and find the user with the specified id (None (default value) if not found)
    specific_user = next((user for user in users if user["id"] == int(id)), None)
    # if user is not found
    if specific_user is None:
        result = {"message": "user not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    # otherwise user has been found so we return a success message and the user data (json)
    result = {"message": "user successfully found", "data": specific_user}
    return jsonify(result)


# DELETE -> specific user -> JSON
@app.delete("/users/<id>")
def delete_user(id):
    # search through users list and find the user with the specified id (None (default value) if not found)
    specific_user = next((user for user in users if user["id"] == int(id)), None)
    # if user is not found
    if specific_user is None:
        result = {"message": "user not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404

    # otherwise user has been found so we return a success message and the user data (json)
    # delete user from users list
    users.remove(specific_user)
    result = {"message": "user successfully deleted", "data": specific_user}
    return jsonify(result)


# PUT -> request.json -> update specific user -> JSON
@app.put("/users/<id>")
def update_user(id):
    # get update data from PUT request body
    update_data = request.json
    # search through users list and find the user with the specified id (None (default value) if not found)
    specific_user = next((user for user in users if user["id"] == int(id)), None)
    # if user is not found
    if specific_user is None:
        result = {"message": "user not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404

    # otherwise user has been found so we return a success message and user data (json)
    # update all values in "specific_user" with values from "update_data" dictionary
    # it changes in place due to us accessing values via memory address ("next" function)
    specific_user.update(update_data)
    # check if it has been updated and changed in the "users" list successfully
    # print(specific_user)
    # print(users)

    result = {"message": "user has been successfully updated", "data": specific_user}
    return jsonify(result)


# POST -> request.json -> create user and add to users list -> json
@app.post("/users")
def create_user():
    new_user = request.json
    user_ids = [user["id"] for user in users]
    # print(user_ids) # check if you have got all the ids successfully
    max_id = max(user_ids)
    # print(max_id) # check if you have max id sucessfully
    new_user["id"] = max_id + 1
    # print(new_user) # check if new user has been crafted successfully

    # add to users list of dict
    users.append(new_user)
    # create message to return
    result = {"message": "user successfully added", "data": new_user}
    # added appropriate status code
    return jsonify(result), 201


# ************ CRUD OPERATIONS FOR POLICIES ***************************************************************************************************************
# GET -> all policies -> JSON
@app.get("/policies-data")
def get_policies():
    # have to convert to JSON (using jsonify library from Flask)
    return jsonify(policies)


# GET -> specific policy -> JSON
@app.get("/policiesdata/<id>")
def get_policy(id):
    # search through policies list and find the policy with the specified id (None (default value) if not found)
    specific_policy = next(
        (policy for policy in policies if policy["id"] == int(id)), None
    )
    # if policy is not found
    if specific_policy is None:
        result = {"message": "policy not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    # otherwise policy has been found so we return a success message and the policy data (json)
    result = {"message": "policy successfully found", "data": specific_policy}
    return jsonify(result)


# DELETE -> specific policy -> JSON
@app.delete("/policiesdata/<id>")
def delete_policy(id):
    # search through policies list and find the policy with the specified id (None (default value) if not found)
    specific_policy = next(
        (policy for policy in policies if policy["id"] == int(id)), None
    )
    # if policy is not found
    if specific_policy is None:
        result = {"message": "policy not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404

    # otherwise policy has been found so we return a success message and the policy data (json)
    # delete policy from policies list
    policies.remove(specific_policy)
    result = {"message": "policy successfully deleted", "data": specific_policy}
    return jsonify(result)


# PUT -> request.json -> update specific policy -> JSON
@app.put("/policiesdata/<id>")
def update_policy(id):
    # get update data from PUT request body
    update_data = request.json
    # search through policies list and find the policy with the specified id (None (default value) if not found)
    specific_policy = next(
        (policy for policy in policies if policy["id"] == int(id)), None
    )
    # if policy is not found
    if specific_policy is None:
        result = {"message": "policy not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404

    # otherwise policy has been found so we return a success message and policy data (json)
    # update all values in "specific_policy" with values from "update_data" dictionary
    # it changes in place due to us accessing values via memory address ("next" function)
    specific_policy.update(update_data)
    # check if it has been updated and changed in the "policies" list successfully
    # print(specific_policy)
    # print(policies)

    result = {
        "message": "policy has been successfully updated",
        "data": specific_policy,
    }
    return jsonify(result)


# POST -> request.json -> create policy and add to policies list -> json
@app.post("/policiesdata")
def create_policy():
    new_policy = request.json
    policy_ids = [policy["id"] for policy in policies]
    # print(policy_ids) # check if you have got all the ids successfully
    max_id = max(policy_ids)
    # print(max_id) # check if you have max id sucessfully
    new_policy["id"] = max_id + 1
    # print(new_policy) # check if new policy has been crafted successfully

    # add to policies list of dict
    policies.append(new_policy)
    # create message to return
    result = {"message": "policy successfully added", "data": new_policy}
    # added appropriate status code
    return jsonify(result), 201
