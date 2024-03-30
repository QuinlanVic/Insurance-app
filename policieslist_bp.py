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
