from flask import Blueprint, render_template, redirect, url_for, request, abort, flash

from flask_wtf import FlaskForm

from extensions import db

from models.user import User, UserPolicy, UserClaim

from werkzeug.security import generate_password_hash, check_password_hash

# from django.utils.http import url_has_allowed_host_and_scheme

user_bp = Blueprint("user", __name__)


# from + import combo to only import what we need to improve performance
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_login import login_user, login_required, logout_user


# signup validation
class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=6)])
    email = EmailField("Email", validators=[InputRequired()])
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

        # if it does exist then user cannot sign up and send them back to signup page
        if specific_user:
            # the message below is displayed in the "div" in the signup form
            raise ValidationError("Email already exists")


# login validation
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    # do not have special validators so hacker cannot know proper length of passwords and such unless they go to signup
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
            # the message below is displayed in the "div" in the signup form
            raise ValidationError("Email or password is invalid")

    # Validate for login form
    def validate_password(self, field):
        # access email via self
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if not check_password_hash(user.password, field.data):
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
        # go to homepage
        # token is issued - cookies stored in the browser
        login_user(specific_user)
        flash("You have been successfully logged in " + f"{specific_user.name} :)")
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
# new route for signup page
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
        # "id" should be auto-created and "pic" and "policy-id" should have empty strings as default values
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            # log the user in
            login_user(new_user)
            # go to home page when posting from signup page
            flash("You have successfully signed up " + f"{new_user.name} :)")
            next = request.args.get("next")
            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # if not url_has_allowed_host_and_scheme(next, request.host):
            #     return abort(400)
            # return f"<h1>Welcome back, {specific_user.name}"
            return redirect(next or url_for("main.index_page"))
        # return render_template("profile.html", new_user.to_dict())
        except Exception as e:
            db.session.rollback()  # undo the change (unless committed already)
            return f"<h1>An error occured: {str(e)}<\h1>", 500

    # only on GET
    # then use "form" in signup page
    return render_template("signup.html", form=form)


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out :)")
    return redirect(url_for("main.index_page"))


@user_bp.route("/takeoutpolicy", methods=["POST"])
@login_required
def take_out_policy():
    # get the user's id and the policy's id and add to this new table
    new_user_policy = UserPolicy(
        user_id=request.form.get("user_id"), policy_id=request.form.get("policy_id")
    )
    # do some database stuff here later
    try:
        # try to add the new policy
        db.session.add(new_user_policy)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Undo the change (cannot be done if already committed)
        return f"<h1>An error occured: {str(e)}</h1>", 500
    flash("You have successfully applied for a new policy!")
    flash("We will inform you via email whether it is successful or not :)")
    return redirect(url_for("policieslist.policies_list_page"))


# store tokens in browser (local storage or cookies) (gets given after signing up/logging in)
# no token, no data
