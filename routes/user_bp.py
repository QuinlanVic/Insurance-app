from flask import Blueprint, render_template, redirect, url_for, request, abort, flash

from flask_wtf import FlaskForm

from extensions import db

from models.user import User

# from django.utils.http import url_has_allowed_host_and_scheme

user_bp = Blueprint("user", __name__)


# from + import combo to only import what we need to improve performance
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_login import login_user, logout_user, login_required


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
@user_bp.route("/login", methods=["GET", "POST"])  # HOF
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
        if not specific_user:
            return render_template("login.html", form=form)
        # otherwise user has logged in successfully
        # go to homepage when posting from login page
        # token is issued - cookies stored in the browser
        login_user(specific_user)
        flash("You have been successfully logged in " + f"{specific_user.username} :)")
        next = request.args.get("next")
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return abort(400)
        # return f"<h1>Welcome back, {specific_user.name}"
        return redirect(next or url_for("main.index_page"))

    # only on GET
    # use "form" in login page
    return render_template("login.html", form=form)


# GET - Issue token
# POST - Verify token
# new route for register page
@user_bp.route("/signup", methods=["GET", "POST"])  # HOF
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
            # go to profile page when posting from signup page
            # print("Profile page", name, email, password)
            # return render_template("profile.html", user=new_user)
            return "<h1> Registration successful </h1>", 201
        # now send them to new profile page
        # return render_template("profile.html", new_user.to_dict())
        except Exception as e:
            db.session.rollback()  # undo the change (unless committed already)
            return f"<h1>An error occured: {str(e)}", 500

    # only on GET
    # then use "form" in signup page
    return render_template("signup.html", form=form)


# store tokens in browser (local storage or cookies) (gets given after signing up/logging in)
# no token, no data
