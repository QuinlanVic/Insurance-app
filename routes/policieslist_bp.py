from flask import Blueprint, render_template, request

from app import Policy, db

import json

policieslist_bp = Blueprint("policieslist", __name__)

# ********* All POLICIESLIST URLS ***********
# Defines View part of web application


# policies list
@policieslist_bp.route("/")
def policies_list_page():
    policy_list = Policy.query.all()  # SELECT * FROM policies | policy_list iterator
    # print(type(policy_list)) # list
    # print(type(policy_list[0])) # app.policy
    data = [policy.to_dict() for policy in policy_list]  # convert to a list of dict
    return render_template("policies_list.html", policies=data)


# specific policy page
@policieslist_bp.route("/<id>")
def policy_page(id):
    specific_policy = Policy.query.get(id)

    if specific_policy is None:
        return "<h1>Policy not found</h1>"

    return render_template("Policy.html", policy=specific_policy.to_dict())


# /policieslist/add -> Add policy form -> Submit -> /policieslist
@policieslist_bp.route("/add")
def add_policy_page():
    return render_template("addpolicy.html")


# /policieslist/update -> Update policy form -> Submit -> /policieslist
# Has to be post to pass the data via body ("GET" uses URL)
# take you to update form with data after manipulation
@policieslist_bp.route("/update", methods=["POST"])
def update_policy_page():
    # get the policy
    policy = request.form.get("policy")
    # test its dtype and if it's the correct one
    print(policy)
    print(type(policy))
    # funny error as JSON only supports single quotes LOLOLOLOLOL
    policy_json = policy.replace("'", '"')
    # convert into a dict
    policy_dict = json.loads(policy_json)
    print(type(policy_dict))
    # go to update policy form
    return render_template("updatepolicy.html", policy=policy_dict)


# ***** FORM ACTION CRUD OPERATIONS *****


# ADD policy TO SQL DATABASE NOW (NOT LOCAL)
@policieslist_bp.route("/", methods=["POST"])
def new_policy_list():
    # get all form data
    policy_name = request.form.get("name")
    policy_price = request.form.get("price")
    policy_poster = request.form.get("poster")
    policy_desc = request.form.get("desc")
    # create new policy
    new_policy = Policy(
        name=policy_name,
        price=policy_price,
        poster=policy_poster,
        desc=policy_desc,
    )
    try:
        # try to add the new policy
        db.session.add(new_policy)
        db.session.commit()
        # get all policies
        policy_list = Policy.query.all()
        # convert to a list of dict
        data = [policy.to_dict() for policy in policy_list]
        # go back to policies page after adding new policy
        # return render_template("policies_list.html", policys=data)
        return f"{new_policy.name} successfully created"
    except Exception as e:
        db.session.rollback()  # Undo the change (cannot be done if already committed)
        return f"<h1>An error occured: {str(e)}", 500


# UPDATE policy FORM TO SQL DATABASE NOW NOT LOCAL
# has to be a different url or it will do the other "/update" above as
# it also uses a POST method because it has to for passing data via body ("GET" uses URL)
@policieslist_bp.route("/update/db", methods=["POST"])
def update_policy_list():
    # get all form data
    policy_id = request.form.get("id")
    policy_name = request.form.get("name")
    policy_price = request.form.get("price")
    policy_poster = request.form.get("poster")
    policy_desc = request.form.get("desc")
    # set up update data dict
    update_data = {
        "name": policy_name,
        "price": policy_price,
        "poster": policy_poster,
        "desc": policy_desc,
    }
    # get specific policy to update
    specific_policy = Policy.query.get(policy_id)
    if specific_policy is None:
        return "<h1>Policy not found</h1>"
    try:
        # update all values in "specific_policy" with values from "update_data" dictionary
        # loop body as you only want to work with specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change it which is unsafe!!!!
            # specific_policy.key = update_data.get(key, specific_policy.key)
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_policy, key):
                # now update those values
                setattr(specific_policy, key, value)
        db.session.commit()
        # now take them to the policy page
        # return f"{specific_policy.name} successfully updated", render_template("policy.html", policy=specific_policy)
        return f"{specific_policy.name} successfully updated"
    except Exception as e:
        return f"<h1>An error occured: {str(e)}"


# delete policy from db after pressing button
@policieslist_bp.route("/delete", methods=["POST"])
def delete_policy_by_id():
    # get name from form
    id = request.form.get("policy_id")
    # get the specific policy
    policy = Policy.query.get(id)
    # test if we found the correct id value
    # print(request.form.get("policy_id"))
    # policy = Policy.query.get(id)
    if not policy:
        # return jsonify({"message": "Policy not found"}), 404
        # Do not return JSON data as you want to display the information on the screen
        return "<h1>Policy not found</h1>", 404
    # otherwise delete it
    try:
        db.session.delete(policy)
        db.session.commit()
        # return jsonify({"message": "Policy deleted successfully", "data": policy.to_dict()})
        # Do not return JSON data as you want to display the information on the screen
        return f"<h1>{policy.to_dict()['name']} successfully deleted</h1>"
    except Exception as e:
        # return jsonify({"error": str(e)})
        # Do not return JSON data as you want to display the information on the screen to the user
        return f"<h1>An error occured: {str(e)}</h1>", 500


# ***** ALL OLD POLICIES PAGE ROUTES *****
# policy page
# @app.route("/policies/<id>")
# def policy_page(id):
#     # policy = get_policy(id)
#     # print(type(policy))
#     # search through policies list and find the policy with the specified id (None (default value) if not found)
#     print(id)
#     specific_policy = next(
#         (policy for policy in policies if policy["id"] == int(id)), None
#     )
#     # if policy is not found
#     if specific_policy is None:
#         # result = {"message": "policy not found"}
#         # return a not found message and appropriate status code (json)
#         return "<h1>Error: Policy not found :(</h1>"
#     # otherwise policy has been found so we return a success message and the policy data (json)
#     # result = {"message": "policy successfully found", "data": specific_policy}
#     # return jsonify(result)
#     return render_template("policy.html", policy=specific_policy)
