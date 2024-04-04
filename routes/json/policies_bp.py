from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models.policy import Policy
from extensions import db

# ********** THESE ARE FOR JSON REQUESTS BY FRONT-END DEVELOPERS **********

# or no import and this code
# class Policy(db.Model):
#     __tablename__ = "policies"
#     # automatically creates and assigns value
#     # increased performance if you do not do calculations to update id by max id on the python side
#     # if autoincremented on the SQL side it will not have a decrease in preformance as it will remember the last value and update easily
#     # increased security as it is more difficult for people to guess "id" values
#     # easier to merge two tables as their id primary keys will not be the same/consist of duplicates
#     id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float(50), nullable=False)
#     # give defaults to these values as we or users can update them in future
#     poster = db.Column(db.String(255), default="")
#     desc = db.Column(db.String(500), default="")

#     # JSON - Keys (can change names sent to front-end)
#     # class method
#     # dict is also easier to convert to JSON
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "price": self.price,
#             "poster": self.poster,
#             "desc": self.desc,
#         }
# db = SQLALchemy()

# create new instance of Blueprint class called "policies"
policies_bp = Blueprint("policies", __name__)


# ONLY JSON REQUESTS TO DATABASE


# Get all policies from azure request
@policies_bp.get("/")
def get_policies():
    policy_list = Policy.query.all()  # SELECT * FROM policies | policy_list iterator
    data = [policy.to_dict() for policy in policy_list]  # convert to a list of dict
    # print(data)
    # print(type(jsonify(data)))
    # return jsonify(data)
    return data


# Get a specific policy from azure request
@policies_bp.get("/<id>")
def get_specific_policy(id):
    # print(type(id))  # string

    # get specific policy
    specific_policy = Policy.query.get(id)

    if specific_policy is None:
        result = {"message": "policy not found"}
        return jsonify(result), 404

    # convert to a dictionary to put in JSON
    data = specific_policy.to_dict()
    result = {"message": "policy successfully found", "data": data}
    return jsonify(result)


# Create a new policy and add it to azure db request
@policies_bp.post("/")
def create_policy():
    # get new policy JSON data from body in request
    data = request.json
    # create a new policy with it, no id as it is automatically created and assigned
    new_policy = Policy(
        name=data["name"],
        price=data["price"],
        poster=data["poster"],
        desc=data["desc"],
    )
    # if keys of Model and keys of data sent from users side are the same then you can use unpacking
    # risk = if they provide an "id" value, it is added (not automatically generated)
    # new_policy = policy(**data)
    try:
        db.session.add(new_policy)
        db.session.commit()
        # check if policy is correctly updated
        print(new_policy)
        # create message to return
        result = {"message": "policy added successfully", "data": new_policy.to_dict()}
        # added status code
        return jsonify(result), 201
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured": str(e)}
        return jsonify(result), 500


# Update specific policy and add to azure db request
@policies_bp.put("/<id>")
def update_policy(id):
    # get data from request body
    update_data = request.json
    # get specific policy
    specific_policy = Policy.query.get(id)
    # if not found
    if specific_policy is None:
        result = {"message": "policy not found"}
        return jsonify(result), 404
    try:
        # update all values in "specific_policy" with values from "update_data" dictionary
        # loop request body data (update_data) as you only want to work with the specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change our db which is unsafe!!!!
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_policy, key):
                # update the value of that key
                setattr(specific_policy, key, value)
                # commit changes after all keys have been updated
        db.session.commit()
        # check if policy was correctly updated
        # print(specific_policy)
        result = {
            "messsage": "policy successfully updated",
            "data": specific_policy.to_dict(),
        }
        return jsonify(result)
    # if an error occured while updating
    except Exception as e:
        db.session.rollback()  # undo the changes (unless they have already been committed)
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500


# Delete the specific policy from azure db request
@policies_bp.delete("/<id>")
def delete_policy(id):
    # get specific policy from "id" in URL
    policy_del = Policy.query.get(id)
    # if we did not find it
    if not policy_del:
        result = {"message": "policy not found"}
        return jsonify(result), 404
    try:
        # delete from database
        db.session.delete(policy_del)
        # making the change permanent
        db.session.commit()
        result = {
            "messsage": "policy successfully deleted",
            "data": policy_del.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500


# ***************** THESE ARE OLD JSON REQUESTS BY FRONT-END DEVELOPERS FOR POLICIES USING LOCAL DATA *******************
# # GET -> all policies -> JSON
# @app.get("/policies-data")
# def get_policies():
#     # have to convert to JSON (using jsonify library from Flask)
#     return jsonify(policies)


# # GET -> specific policy -> JSON
# @app.get("/policiesdata/<id>")
# def get_policy(id):
#     # search through policies list and find the policy with the specified id (None (default value) if not found)
#     specific_policy = next(
#         (policy for policy in policies if policy["id"] == int(id)), None
#     )
#     # if policy is not found
#     if specific_policy is None:
#         result = {"message": "policy not found"}
#         # return a not found message and appropriate status code (json)
#         return jsonify(result), 404
#     # otherwise policy has been found so we return a success message and the policy data (json)
#     result = {"message": "policy successfully found", "data": specific_policy}
#     return jsonify(result)


# # DELETE -> specific policy -> JSON
# @app.delete("/policiesdata/<id>")
# def delete_policy(id):
#     # search through policies list and find the policy with the specified id (None (default value) if not found)
#     specific_policy = next(
#         (policy for policy in policies if policy["id"] == int(id)), None
#     )
#     # if policy is not found
#     if specific_policy is None:
#         result = {"message": "policy not found"}
#         # return a not found message and appropriate status code (json)
#         return jsonify(result), 404

#     # otherwise policy has been found so we return a success message and the policy data (json)
#     # delete policy from policies list
#     policies.remove(specific_policy)
#     result = {"message": "policy successfully deleted", "data": specific_policy}
#     return jsonify(result)


# # PUT -> request.json -> update specific policy -> JSON
# @app.put("/policiesdata/<id>")
# def update_policy(id):
#     # get update data from PUT request body
#     update_data = request.json
#     # search through policies list and find the policy with the specified id (None (default value) if not found)
#     specific_policy = next(
#         (policy for policy in policies if policy["id"] == int(id)), None
#     )
#     # if policy is not found
#     if specific_policy is None:
#         result = {"message": "policy not found"}
#         # return a not found message and appropriate status code (json)
#         return jsonify(result), 404

#     # otherwise policy has been found so we return a success message and policy data (json)
#     # update all values in "specific_policy" with values from "update_data" dictionary
#     # it changes in place due to us accessing values via memory address ("next" function)
#     specific_policy.update(update_data)
#     # check if it has been updated and changed in the "policies" list successfully
#     # print(specific_policy)
#     # print(policies)

#     result = {
#         "message": "policy has been successfully updated",
#         "data": specific_policy,
#     }
#     return jsonify(result)


# # POST -> request.json -> create policy and add to policies list -> JSOn
# @app.post("/policiesdata")
# def create_policy():
#     new_policy = request.json
#     policy_ids = [policy["id"] for policy in policies]
#     # print(policy_ids) # check if you have got all the ids successfully
#     max_id = max(policy_ids)
#     # print(max_id) # check if you have max id sucessfully
#     new_policy["id"] = max_id + 1
#     # print(new_policy) # check if new policy has been crafted successfully

#     # add to policies list of dict
#     policies.append(new_policy)
#     # create message to return
#     result = {"message": "policy successfully added", "data": new_policy}
#     # added appropriate status code
#     return jsonify(result), 201
