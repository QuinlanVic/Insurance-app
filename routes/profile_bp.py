from flask import Blueprint, render_template, redirect, url_for, request, flash

from models.user import User, UserPolicy, UserClaim
from models.policy import Policy
from extensions import db

from werkzeug.security import generate_password_hash

from flask_login import login_required

import json

profile_bp = Blueprint("profile", __name__)

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


# Define a route for the claims page
@profile_bp.route("/claims/<id>")
@login_required
def claims_page(id):
    claims = UserClaim.query.get(id)
    if claims is None:
        return render_template("noclaims.html")
    return render_template("claims.html", claims=claims.to_dict())


# Define a route for the claims page
@profile_bp.route("/mypolicies/<id>")
@login_required
def my_policies_page(id):
    # get all policies that the user has
    user_policies = UserPolicy.query.get(id)
    user_policies_data = [user_policy.to_dict() for user_policy in user_policies]
    policies = [
        Policy.query.get(user_policy_data["policy_id"])
        for user_policy_data in user_policies_data
    ]
    if policies is None:
        return render_template("nopolicies.html")
    return render_template("mypolicies.html", policies=policies.to_dict())


# /profile/update -> Update profile form (existing fields) -> Submit -> /profile/id
# Has to be post to pass the data via body ("GET" uses URL)
# take you to update form with data after manipulation
@profile_bp.route("/update", methods=["POST"])
@login_required
def update_profile_page():
    # get the user
    user = request.form.get("profile")
    print(user)
    print(type(user))
    # funny error as JSON only supports single quotes LOLOLOLOLOL
    user_json = user.replace("'", '"')
    # convert into a dict
    user_dict = json.loads(user_json)
    print(type(user_dict))
    # now render the update profile page with user information
    return render_template("updateprofile.html", user=user_dict)


# ***** FORM ACTION CRUD OPERATIONS *****


# delete user profile from db (after clicking button)
@profile_bp.route("/delete", methods=["POST"])
@login_required
def delete_user_by_id():
    # get name value from form which contains the id value
    id = request.form.get("profile_id")
    # print(id) # test if we found the correct id value
    # get the specific user
    user = User.query.get(id)
    # if the user is not found
    if not user:
        # return jsonify({"message": "user not found"}), 404
        # Do not return JSON data as you want to display the information on the screen
        return "<h1>User not found</h1>", 404
    # otherwise delete user
    try:
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


# update user
# UPDATE PROFILE FORM TO SQL DATABASE NOW NOT LOCAL
# has to be a different url or it will do the other "/update" above as
# it also uses a POST method because it has to for passing data via body ("GET" uses URL)
@profile_bp.route("/update/db", methods=["POST"])
@login_required
def update_profile():
    user_id = request.form.get("id")
    user_name = request.form.get("name")
    user_email = request.form.get("email")
    user_password = generate_password_hash(request.form.get("password"))
    user_pic = request.form.get("pic")
    user_policy_id = request.form.get("policy_id")
    update_data = {
        "name": user_name,
        "email": user_email,
        "password": user_password,
        "pic": user_pic,
        "policy_id": user_policy_id,
    }
    specific_user = User.query.get(user_id)
    if specific_user is None:
        return "<h1>user not found</h1>"
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
        flash(f"{specific_user.name} " + "successfully updated")
        next = request.args.get("next")
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return abort(400)
        # return f"<h1>Welcome back, {specific_user.name}"
        return redirect(next or url_for("main.index_page"))
    except Exception as e:
        return f"<h1>An error occured: {str(e)}</h1>"
