from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models.user import User
from extensions import db

from flask_login import login_required

# ********** THESE ARE FOR JSON REQUESTS BY FRONT-END DEVELOPERS **********

# or no import and this code
# class User(db.Model):
#     __tablename__ = "users"
#     # automatically creates and assigns value
#     id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(db.String(100), nullable=False)
#     # make unique
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     # give defaults to these values and we or users can update them in future
#     pic = db.Column(db.String(255), default="")
#     user_id = db.Column(db.String(50), default="0")

#     # JSON - Keys (can change names sent to front-end)
#     # class method
#     # dict is also easier to convert to JSON
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "email": self.email,
#             "password": self.password,
#             "pic": self.pic,
#             "user_id": self.user_id,
#         }
# db = SQLAlchecmy()

# create new instance of Bluerint class called "users"
users_bp = Blueprint("users", __name__)


# Get all users from azure request
@users_bp.get("/")
@login_required
def get_users():
    user_list = User.query.all()  # SELECT * FROM users | user_list iterator
    data = [user.to_dict() for user in user_list]  # convert to a list of dict
    # print(data)
    # print(type(jsonify(data)))
    # return jsonify(data)
    return data


# Get a specific user from azure request
@users_bp.get("/<id>")
@login_required
def get_specific_user(id):
    # print(type(id))  # string

    # get specific user
    specific_user = User.query.get(id)

    if specific_user is None:
        result = {"message": "user not found"}
        return jsonify(result), 404

    # convert to a dictionary to put in JSON
    data = specific_user.to_dict()
    result = {"message": "user successfully found", "data": data}
    return jsonify(result)


# Create a new user and add it to azure db request
@users_bp.post("/")
@login_required
def create_user():
    # get new user JSON data from body in request
    data = request.json
    # create a new user with it, no id as it is automatically created and assigned
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        pic=data["pic"],
    )
    # if keys of Model and keys of data sent from users side are the same then you can use unpacking
    # risk = if they provide an "id" value, it is added (not automatically generated)
    # new_user = user(**data)
    try:
        db.session.add(new_user)
        db.session.commit()
        # check if user is correctly updated
        print(new_user)
        # create message to return
        result = {"message": "user added successfully", "data": new_user.to_dict()}
        # added status code
        return jsonify(result), 201
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured": str(e)}
        return jsonify(result), 500


# Update specific user and add to azure db request
@users_bp.put("/<id>")
@login_required
def update_user(id):
    # get data from request body
    update_data = request.json
    # get specific user
    specific_user = User.query.get(id)
    # if not found
    if specific_user is None:
        result = {"message": "user not found"}
        return jsonify(result), 404
    try:
        # update all values in "specific_user" with values from "update_data" dictionary
        # loop request body data (update_data) as you only want to work with the specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change our db which is unsafe!!!!
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_user, key):
                # update the value of that key
                setattr(specific_user, key, value)
                # commit changes after all keys have been updated
        db.session.commit()
        # check if user was correctly updated
        # print(specific_user)
        result = {
            "messsage": "user successfully updated",
            "data": specific_user.to_dict(),
        }
        return jsonify(result)
    # if an error occured while updating
    except Exception as e:
        db.session.rollback()  # undo the changes (unless they have already been committed)
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500


# Delete the specific user from azure db request
@users_bp.delete("/<id>")
@login_required
def delete_user(id):
    # get specific user from "id" in URL
    user_del = User.query.get(id)
    # if we did not find it
    if not user_del:
        result = {"message": "user not found"}
        return jsonify(result), 404
    try:
        # delete from database
        db.session.delete(user_del)
        # making the change permanent
        db.session.commit()
        result = {
            "messsage": "user successfully deleted",
            "data": user_del.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500


# ***************** THESE ARE OLD JSON REQUESTS BY FRONT-END DEVELOPERS FOR USERS USING LOCAL DATA *******************
# ************ CRUD OPERATIONS FOR USER *********************************************************************************************
# # GET -> all users -> JSON
# @app.get("/users")
# def get_users():
#     # have to convert to JSON (using jsonify library from Flask)
#     return jsonify(users)


# # GET -> specific user -> JSON
# @app.get("/users/<id>")
# def get_user(id):
#     # search through users list and find the user with the specified id (None (default value) if not found)
#     specific_user = next((user for user in users if user["id"] == int(id)), None)
#     # if user is not found
#     if specific_user is None:
#         result = {"message": "user not found"}
#         # return a not found message and appropriate status code (json)
#         return jsonify(result), 404
#     # otherwise user has been found so we return a success message and the user data (json)
#     result = {"message": "user successfully found", "data": specific_user}
#     return jsonify(result)


# # DELETE -> specific user -> JSON
# @app.delete("/users/<id>")
# def delete_user(id):
#     # search through users list and find the user with the specified id (None (default value) if not found)
#     specific_user = next((user for user in users if user["id"] == int(id)), None)
#     # if user is not found
#     if specific_user is None:
#         result = {"message": "user not found"}
#         # return a not found message and appropriate status code (json)
#         return jsonify(result), 404

#     # otherwise user has been found so we return a success message and the user data (json)
#     # delete user from users list
#     users.remove(specific_user)
#     result = {"message": "user successfully deleted", "data": specific_user}
#     return jsonify(result)


# # PUT -> request.json -> update specific user -> JSON
# @app.put("/users/<id>")
# def update_user(id):
#     # get update data from PUT request body
#     update_data = request.json
#     # search through users list and find the user with the specified id (None (default value) if not found)
#     specific_user = next((user for user in users if user["id"] == int(id)), None)
#     # if user is not found
#     if specific_user is None:
#         result = {"message": "user not found"}
#         # return a not found message and appropriate status code (json)
#         return jsonify(result), 404

#     # otherwise user has been found so we return a success message and user data (json)
#     # update all values in "specific_user" with values from "update_data" dictionary
#     # it changes in place due to us accessing values via memory address ("next" function)
#     specific_user.update(update_data)
#     # check if it has been updated and changed in the "users" list successfully
#     # print(specific_user)
#     # print(users)

#     result = {"message": "user has been successfully updated", "data": specific_user}
#     return jsonify(result)


# # POST -> request.json -> create user and add to users list -> json
# @app.post("/users")
# def create_user():
#     new_user = request.json
#     user_ids = [user["id"] for user in users]
#     # print(user_ids) # check if you have got all the ids successfully
#     max_id = max(user_ids)
#     # print(max_id) # check if you have max id sucessfully
#     new_user["id"] = max_id + 1
#     # print(new_user) # check if new user has been crafted successfully

#     # add to users list of dict
#     users.append(new_user)
#     # create message to return
#     result = {"message": "user successfully added", "data": new_user}
#     # added appropriate status code
#     return jsonify(result), 201
