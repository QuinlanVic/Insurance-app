from flask import Flask, jsonify, request, render_template

# Create a instance of Flask
app = Flask(__name__) 

# some dummy employee data
employees = [
    {
        "id": 1,
        "name": "Paul Flex",
        "job-title": "CEO",
        "pic": "https://t4.ftcdn.net/jpg/06/35/15/47/360_F_635154757_zU5ZxxZe3Vs0hrrOQ9WBgNgX8s4Cw19s.jpg",
        "desc": "Paul Flex is CoolWater's Chief Executive Officer"
    },
    {
        "id": 2,
        "name": "Sarah Blue",
        "job-title": "CFO",
        "pic": "https://t4.ftcdn.net/jpg/06/12/73/89/360_F_612738927_LIcFCiKHQhHq9R1QhkVRKvT6RelYUmgv.jpg",
        "desc": "Sarah Bleu is CoolWater's Chief Financial Officer"
    },
    {
        "id": 3,
        "name": "Mandla Ngcobo",
        "job-title": "CHRO",
        "pic": "https://www.goodthingsguy.com/wp-content/uploads/2020/07/vusi-thembekwayo-biography-age-net-worth-wife-2.jpg",
        "desc": "Mandla Ngcobo is Coolwater's Chief Human Resources Officer"
    }
]

# some dummy policy data
policies = [
    {
        "id": 1,
        "name": "Cool Car Insurance",
        "price": 1000,
        "poster": "",
        "desc": ""
    },
    {
        "id": 2,
        "name": "Water Car Insurance",
        "price": 1500,
        "poster": "",
        "desc": ""
    },
    {
        "id": 3,
        "name": "CoolWater Car Insurance",
        "price": 2000,
        "poster": "",
        "desc": ""
    },
    {
        "id": 4,
        "name": "CoolCool Car Insurance",
        "price": 2500,
        "poster": "",
        "desc": ""
    },
    {
        "id": 5,
        "name": "WaterCool Car Insurance",
        "price": 3000,
        "poster": "",
        "desc": ""
    }
]

# some dummy user data
users = [
    {
        "id": 1,
        "name": "Ethan Rich",
        "email": "E.rich@gmail.com",
        "pic": "",
    },
    {
        "id": 2,
        "name": "Scarlet Ndlovu",
        "email": "Scar.let@gmail.com",
        "pic": "",
    },
    {
        "id": 3,
        "name": "Bertha Pudding",
        "email": "Bertha@gmail.com",
        "pic": "",
    }
]

# root URL 
@app.route("/")
def home_page():
    return render_template("index.html")

# policies page
@app.route("/policies")
def policies_page():
    return render_template("policies.html", policies=policies) 

# policy page 
@app.route("/policies/<id>")
def policy_page(id):
    return render_template("policy.html")

# Define a route for the /about URL
@app.route("/about")
def about_page():
    return render_template("about.html", employees=employees)

# Define a route for the /help page
@app.route("/help")
def help_page():
    return render_template("help.html")

# Define a route for the /profile page
@app.route("/profile/<id>") 
def profile_page(id):
    return render_template("profile.html")

# ************ CRUD OPERATIONS FOR USER ************

# GET -> specific user -> JSON
@app.get("/users/<id>")
def get_user(id):
    # search through users list and find the user with the specified id (None (default value) if not found)
    specific_user = next((user for user in users if user["id"] == int(id)), None)
    # if user is not found
    if specific_user is None:
        result = {"message": "user not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    # otherwise user has been found so we return a success message and the user data (json)
    result = {"message": "user successfully found", "data": specific_user}
    return jsonify(result)

# DELETE -> specific user -> JSON
@app.delete("/users/<id>")
def delete_user(id):
    # search through users list and find the user with the specified id (None (default value) if not found)
    specific_user = next((user for user in users if user["id"] == int(id)), None)
     # if user is not found
    if specific_user is None:
        result = {"message": "user not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    
    # otherwise user has been found so we return a success message and the user data (json)
    # delete user from users list
    users.remove(specific_user)
    result = {"message": "user successfully deleted", "data": specific_user}
    return jsonify(result)

# PUT -> request.json -> update specific user -> JSON 
@app.put("/users/<id>")
def update_user(id):
    # get update data from PUT request body
    update_data = request.json
    # search through users list and find the user with the specified id (None (default value) if not found)
    specific_user = next((user for user in users if user["id"] == int(id)), None)
     # if user is not found
    if specific_user is None:
        result = {"message": "user not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    
    # otherwise user has been found so we return a success message and user data (json)
    # update all values in "specific_user" with values from "update_data" dictionary
    # it changes in place due to us accessing values via memory address ("next" function)
    specific_user.update(update_data)
    # check if it has been updated and changed in the "users" list successfully
    # print(specific_user)
    # print(users)

    result = {"message": "user has been successfully updated", "data": specific_user}
    return jsonify(result)

# POST -> request.json -> create user and add to users list -> json
@app.post("/users")
def create_user():
    new_user = request.json
    user_ids = [user["id"] for user in users]
    # print(user_ids) # check if you have got all the ids successfully
    max_id = max(user_ids)
    # print(max_id) # check if you have max id sucessfully
    new_user["id"] = max_id + 1
    # print(new_user) # check if new user has been crafted successfully

    # add to users list of dict
    users.append(new_user)
    # create message to return
    result = {"message": "user successfully added", "data": new_user}
    # added appropriate status code
    return jsonify(result), 201

# ************ CRUD OPERATIONS FOR POLICIES ************
# GET -> specific policy -> JSON
@app.get("/policies/<id>")
def get_policy(id):
    # search through policies list and find the policy with the specified id (None (default value) if not found)
    specific_policy = next((policy for policy in policies if policy["id"] == int(id)), None)
    # if policy is not found
    if specific_policy is None:
        result = {"message": "policy not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    # otherwise policy has been found so we return a success message and the policy data (json)
    result = {"message": "policy successfully found", "data": specific_policy}
    return jsonify(result)

# DELETE -> specific policy -> JSON
@app.delete("/policies/<id>")
def delete_policy(id):
    # search through policies list and find the policy with the specified id (None (default value) if not found)
    specific_policy = next((policy for policy in policies if policy["id"] == int(id)), None)
     # if policy is not found
    if specific_policy is None:
        result = {"message": "policy not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    
    # otherwise policy has been found so we return a success message and the policy data (json)
    # delete policy from policies list
    policies.remove(specific_policy)
    result = {"message": "policy successfully deleted", "data": specific_policy}
    return jsonify(result)

# PUT -> request.json -> update specific policy -> JSON 
@app.put("/policies/<id>")
def update_policy(id):
    # get update data from PUT request body
    update_data = request.json
    # search through policies list and find the policy with the specified id (None (default value) if not found)
    specific_policy = next((policy for policy in policies if policy["id"] == int(id)), None)
     # if policy is not found
    if specific_policy is None:
        result = {"message": "policy not found"}
        # return a not found message and appropriate status code (json)
        return jsonify(result), 404
    
    # otherwise policy has been found so we return a success message and policy data (json)
    # update all values in "specific_policy" with values from "update_data" dictionary
    # it changes in place due to us accessing values via memory address ("next" function)
    specific_policy.update(update_data)
    # check if it has been updated and changed in the "policies" list successfully
    # print(specific_policy)
    # print(policies)

    result = {"message": "policy has been successfully updated", "data": specific_policy}
    return jsonify(result)

# POST -> request.json -> create policy and add to policies list -> json
@app.post("/policies")
def create_policy():
    new_policy = request.json
    policy_ids = [policy["id"] for policy in policies]
    # print(policy_ids) # check if you have got all the ids successfully
    max_id = max(policy_ids)
    # print(max_id) # check if you have max id sucessfully
    new_policy["id"] = max_id + 1
    # print(new_policy) # check if new policy has been crafted successfully

    # add to policies list of dict
    policies.append(new_policy)
    # create message to return
    result = {"message": "policy successfully added", "data": new_policy}
    # added appropriate status code
    return jsonify(result), 201

# Define a route for the login page
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")


