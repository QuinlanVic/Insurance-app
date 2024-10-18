from flask import Blueprint, render_template, redirect, url_for, request, flash

from flask_wtf import FlaskForm

from werkzeug.security import generate_password_hash

from models.user import User, UserPolicy, UserClaim, Claim
from models.policy import Policy
from extensions import db

from sqlalchemy import select

from werkzeug.security import generate_password_hash

from flask_login import login_required

import json

profile_bp = Blueprint("profile", __name__)

from wtforms import StringField, PasswordField, SubmitField, EmailField, FloatField
from wtforms.validators import InputRequired, Length, ValidationError, Optional

# ********* All PROFILE URLS ***********
# Defines View part of web application


# Define a route for the profile page
@profile_bp.route("/<id>")
@login_required
def profile_page(id):
    profile = User.query.get(id)
    if profile is None:
        return "<h1>Profile not found</h1>"
    return render_template("profile.html", profile=profile.to_dict())


# Define a route for the claims page (user id)
@profile_bp.route("/claims/<id>")
@login_required
def claims_page(id):
    # get all claims that the user has made
    # claims = UserClaim.query.get(id)
    stmt = select(UserClaim).where(UserClaim.user_id == id)
    result = db.session.execute(stmt)
    user_claims = []
    for user_obj in result.scalars():
        user_claims.append(user_obj.claim_id)
    print(user_claims)
    # if they have no claims load this page
    if user_claims == []:
        return render_template("noclaims.html")
    # if they do have claims
    print(user_claims)
    print(type(user_claims))
    # get only claim data
    claims = [
        Claim.query.get(user_claim_data).to_dict() for user_claim_data in user_claims
    ]
    return render_template("claims.html", claims=claims)


# Define a route for the "my policies" page (user id)
@profile_bp.route("/mypolicies/<id>")
@login_required
def my_policies_page(id):
    # get all policies that the user has
    # user_policies = UserPolicy.query.get(id)
    stmt = select(UserPolicy).where(UserPolicy.user_id == id)
    result = db.session.execute(stmt)
    user_policies = []
    for user_obj in result.scalars():
        user_policies.append(user_obj.policy_id)
    print(user_policies)
    # if they have no policies load this page
    if user_policies == []:
        return render_template("nopolicies.html")
    # if they do have policies
    print(type(user_policies))
    # get only the policy data
    policies = [
        Policy.query.get(user_policy_data).to_dict()
        for user_policy_data in user_policies
    ]
    return render_template("mypolicies.html", policies=policies)


# ***** FORM ACTION CRUD OPERATIONS *****


# User wants to terminate their policy
# delete policy from UserPolicy after pressing button
@profile_bp.route("/mypolicies/terminate", methods=["POST"])
def terminate_policy_by_id():
    # get name from form
    id = request.form.get("policy_id")
    # get the specific policy
    user_policy = UserPolicy.query.filter_by(policy_id=id).first()
    # test if we found the correct id value
    # print(request.form.get("policy_id"))
    # policy = Policy.query.get(id)
    if not user_policy:
        # return jsonify({"message": "Policy not found"}), 404
        # Do not return JSON data as you want to display the information on the screen
        return "<h1>Policy not found</h1>", 404
    # otherwise delete it
    try:
        db.session.delete(user_policy)
        db.session.commit()
        policy_name = Policy.query.get(id)
        flash(f"{policy_name.to_dict()['name']} successfully terminated")
        return redirect(url_for("profile.my_policies_page", id=user_policy.user_id))
    except Exception as e:
        # return jsonify({"error": str(e)})
        # Do not return JSON data as you want to display the information on the screen to the user
        return f"<h1>An error occured: {str(e)}</h1>", 500


# User wants to terminate their claim
# delete claim from UserClaim and Claim after pressing button
@profile_bp.route("/claims/terminate", methods=["POST"])
def terminate_claim_by_id():
    # get name from form
    claim_id = request.form.get("claim_id")
    # get the user_claim from usersclaims table
    user_claim = UserClaim.query.filter_by(claim_id=claim_id).first()
    # get the specific claim from claims table
    claim = Claim.query.get(claim_id)
    if not claim:
        # return jsonify({"message": "Policy not found"}), 404
        # Do not return JSON data as you want to display the information on the screen
        return "<h1>Claim not found</h1>", 404
    # otherwise delete claim from claims table and usersclaims table
    try:
        # delete from usersclaims table first
        db.session.delete(user_claim)
        db.session.commit()
        # delete from claims table second
        db.session.delete(claim)
        db.session.commit()
        flash("Claim successfully terminated")
        return redirect(url_for("profile.claims_page", id=user_claim.user_id))
    except Exception as e:
        # return jsonify({"error": str(e)})
        # Do not return JSON data as you want to display the information on the screen to the user
        return f"<h1>An error occured: {str(e)}</h1>", 500


# update user form validation
class UpdateProfileForm(FlaskForm):
    name = StringField("Name", validators=[Optional(), Length(min=6)])
    email = EmailField("Email", validators=[Optional()])
    password = PasswordField("Password", validators=[Optional(), Length(min=8, max=12)])
    pic = StringField("Picture", validators=[Optional()])
    submit = SubmitField("Update profile")

    # use WTF to send user back to signup page if input is invalid
    # automatically runs when the "form.validate_on_submit()" function executes
    # class method (instance and data from user form via field)
    # validate_<field name>
    # def validate_email(self, field):
    #     # inform WTF that there is an error and display it
    #     print("Validate email was called (reg)", field.data)
    #     # only do this if the email has changed
    #     if self.email != field.data:
    #         print(self)
    #         print(self.email, field.data)
    #         # check if there is an existing email
    #         specific_user = User.query.filter_by(email=field.data).first()
    #         # print(specific_user)

    #         # if it does exist then user cannot sign up and send them back to signup page
    #         if specific_user:
    #             # the message below is displayed in the "div" in the signup form
    #             raise ValidationError("Email already exists")


# update profile page
@profile_bp.route("/update/<id>", methods=["GET", "POST"])
@login_required
def update_profile(id):
    form = UpdateProfileForm()
    print("inside of update profile")
    # only on POST (when user is updating profile)
    if form.validate_on_submit():
        print("GOT IN POST")
        # if the email has changed then check if it is already in the database
        user = User.query.get(request.form.get("id"))
        print(user.email)

        # extract data 
        print(form.name.data)
        user_name = form.name.data if form.name.data else user.name
        user_email = form.email.data if form.email.data else user.email
        user_password = generate_password_hash(form.password.data) if form.password.data else user.password
        user_pic = form.pic.data if form.pic.data else user.pic


        # user_id = request.form.get("id")
        # user_name = request.form.get("name")
        # user_email = request.form.get("email")
        # user_password = generate_password_hash(request.form.get("password"))
        # user_pic = request.form.get("pic")
        # user_policy_id = request.form.get("policy_id")
        if user.email != form.email.data:
            # check if there is an existing email
            specific_user = User.query.filter_by(email=form.email.data).first()
            if specific_user:
                flash(f"{form.email.data} " + " email is already taken", "error")
                return render_template("updateprofile.html", form=form, user=user_dict)
            
        # Create a dictionary of the updated data
        update_data = {
            "name": user_name,
            "email": user_email,
            "password": user_password,
            "pic": user_pic,
        }
        specific_user = User.query.get(user.id)
        if specific_user is None:
            flash("User not found", "error")
            return render_template("updateprofile.html", form=form, user=user_dict)
        try:
            # update all values in "specific_user" with values from "update_data" dictionary
            # loop body as you only want to work with specific keys we need to update
            for key, value in update_data.items():
                # if they put in random keys it will change it which is unsafe!!!!
                # specific_user.key = update_data.get(key, specific_user.key)
                # so now we check if the key is in the table and only work with it if it is
                if hasattr(specific_user, key):
                    # now update those values
                    setattr(specific_user, key, value)
            db.session.commit()
            # now take them back to the profile page
            # return f"{specific_user.name} successfully updated", render_template("profile.html")
            flash(f"{specific_user.name} " + "successfully updated", "success")
            next = request.args.get("next")
            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # if not url_has_allowed_host_and_scheme(next, request.host):
            #     return abort(400)
            # return f"<h1>Welcome back, {specific_user.name}"
            return redirect(next or url_for("main.index_page"))
        except Exception as e:
            return f"<h1>An error occured: {str(e)}</h1>"

    # Only on GET
    # get the user
    # user = request.form.get("profile")
    print(form.errors)
    user = User.query.get(id)
    if user is None:
        flash("User not found", "error")
    user_dict = user.to_dict()
    print("This is the user underneath:")
    print(user_dict)
    # now render the update profile page with user information
    return render_template("updateprofile.html", form=form, user=user_dict)


# delete user profile from db (after clicking button)
@profile_bp.route("/delete", methods=["POST"])
@login_required
def delete_user_by_id():
    # get name value from form which contains the id value
    id = request.form.get("profile_id")
    # print(id) # test if we found the correct id value
    # get the specific user
    user = User.query.get(id)
    print(user)
    # get all their policies they have
    user_policies = UserPolicy.query.filter_by(user_id=id).all()
    print(user_policies)
    # get all their claim entries
    user_claims = UserClaim.query.filter_by(user_id=id).all()
    print(user_claims)
    # get all their claims? (maybe keep this as legacy data and it does not include their user id at all)
    # if the user is not found
    if not user:
        # return jsonify({"message": "user not found"}), 404
        # Do not return JSON data as you want to display the information on the screen
        return "<h1>User not found</h1>", 404
    # otherwise delete user
    try:
        # delete policies
        for user_policy in user_policies:
            db.session.delete(user_policy)
            db.session.commit()
        # delete claims
        for user_claim in user_claims:
            db.session.delete(user_claim)
            db.session.commit()
        # then only delete the user
        db.session.delete(user)
        db.session.commit()

        # return jsonify({"message": "user deleted successfully", "data": user.to_dict()})
        # Do not return JSON data as you want to display the information on the screen
        # take them back to home page
        # return f"<h1>{user.to_dict()['name']} successfully deleted</h1>", render_template("index.html")
        flash(f"{user.to_dict()['name']} " + "successfully deleted")
        next = request.args.get("next")
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return abort(400)
        # return f"<h1>Welcome back, {specific_user.name}"
        return redirect(next or url_for("main.index_page"))
    except Exception as e:
        # undo changes (unless already committed)
        db.session.rollback()
        # return jsonify({"An error occured:": str(e)})
        # Do not return JSON data as you want to display the information on the screen to the user
        return f"<h1>An error occured: {str(e)}</h1>", 500
