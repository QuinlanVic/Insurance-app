from flask import Blueprint, render_template, request

from app import User, db

import json

profile_bp = Blueprint("profile", __name__)

# ********* All PROFILE URLS ***********
# Defines View part of web application


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
