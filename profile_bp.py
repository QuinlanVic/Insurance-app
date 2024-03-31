from flask import Blueprint, render_template, request

from app import User, db

import json

profile_bp = Blueprint("profile", __name__)

# ********* All PROFILE URLS ***********
# Defines View part of web application


# Define a route for the /profile page
@profile_bp.route("/<id>")
def profile_page(id):
    profile = User.query.get(id)
    return render_template("profile.html", profile=profile)


# ***** FORM ACTION CRUD OPERATIONS *****


# delete user profile from db (after clicking button)
@profile_bp.route("/delete", methods=["POST"])
def delete_user_by_id():
    # get name value from form which contains the id value
    id = request.form.get("user_id")
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
        return f"<h1>{user.to_dict()['name']} successfully deleted</h1>"
    except Exception as e:
        # undo changes (unless already committed)
        db.session.rollback()
        # return jsonify({"An error occured:": str(e)})
        # Do not return JSON data as you want to display the information on the screen to the user
        return f"<h1>An error occured: {str(e)}</h1>", 500


# /profile/update -> Update profile form (existing fields) -> Submit -> /profile
# Has to be post to pass the data via body ("GET" uses URL)
# take you to update form with data after manipulation
@profile_bp.route("/update", methods=["POST"])
def update_profile_page():
    user = request.form.get("user")
    print(user)
    print(type(user))
    # funny error as JSON only supports single quotes LOLOLOLOLOL
    user_json = user.replace("'", '"')
    # convert into a dict
    user_dict = json.loads(user_json)
    print(type(user_dict))
    # now render the update profile page with user information
    return render_template("update_profile.html", user=user_dict)


# update user
# UPDATE PROFILE FORM TO SQL DATABASE NOW NOT LOCAL
# has to be a different url or it will do the other "/update" above as
# it also uses a POST method because it has to for passing data via body ("GET" uses URL)
@profile_bp.route("/update/db", methods=["POST"])
def update_profile():
    user_id = request.form.get("id")
    user_name = request.form.get("name")
    user_poster = request.form.get("poster")
    user_rating = request.form.get("rating")
    user_summary = request.form.get("summary")
    user_trailer = request.form.get("trailer")
    update_data = {
        "name": user_name,
        "poster": user_poster,
        "rating": user_rating,
        "summary": user_summary,
        "trailer": user_trailer,
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
        return f"{specific_user.name} successfully updated"
    except Exception as e:
        return f"<h1>An error occured: {str(e)}"
