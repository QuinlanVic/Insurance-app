from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models.employee import Employee
from extensions import db

# ********** THESE ARE FOR JSON REQUESTS BY FRONT-END DEVELOPERS **********

# or no import and this code
# class Employee(db.Model):
#     __tablename__ = "employees"
#     # automatically creates and assigns value
#     id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(db.String(100), nullable=False)
#     job_title = db.Column(db.String(100), nullable=False)
#     # give defaults to these values as we or users can update them in future
#     pic = db.Column(db.String(255), default="")
#     desc = db.Column(db.String(500), default="")

#     # JSON - Keys (can change names sent to front-end)
#     # class method
#     # dict is also easier to convert to JSON
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "job_title": self.job_title,
#             "pic": self.pic,
#             "desc": self.desc,
#         }
# db = SQLALchemy()

# create new instance of Blueprint class called "employees"
employees_bp = Blueprint("employees", __name__)


# ONLY JSON REQUESTS TO DATABASE


# Get all employees from azure request
@employees_bp.get("/")
def get_employees():
    # SELECT * FROM employees | employee_list iterator
    employee_list = Employee.query.all()
    # convert to a list of dict
    data = [employee.to_dict() for employee in employee_list]
    # print(data)
    # print(type(jsonify(data)))
    # return jsonify(data)
    return data


# Get a specific employee from azure request
@employees_bp.get("/<id>")
def get_specific_employee(id):
    # print(type(id))  # string

    # get specific employee
    specific_employee = Employee.query.get(id)

    if specific_employee is None:
        result = {"message": "employee not found"}
        return jsonify(result), 404

    # convert to a dictionary to put in JSON
    data = specific_employee.to_dict()
    result = {"message": "employee successfully found", "data": data}
    return jsonify(result)


# Create a new employee and add it to azure db request
@employees_bp.post("/")
def create_employee():
    # get new employee JSON data from body in request
    data = request.json
    # create a new employee with it, no id as it is automatically created and assigned
    new_employee = Employee(
        name=data["name"],
        job_title=data["job_title"],
        pic=data["pic"],
        desc=data["desc"],
    )
    # if keys of Model and keys of data sent from users side are the same then you can use unpacking
    # risk = if they provide an "id" value, it is added (not automatically generated)
    # new_employee = employee(**data)
    try:
        db.session.add(new_employee)
        db.session.commit()
        # check if employee is correctly updated
        print(new_employee)
        # create message to return
        result = {
            "message": "employee added successfully",
            "data": new_employee.to_dict(),
        }
        # added status code
        return jsonify(result), 201
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured": str(e)}
        return jsonify(result), 500


# Update specific employee and add to azure db request
@employees_bp.put("/<id>")
def update_employee(id):
    # get data from request body
    update_data = request.json
    # get specific employee
    specific_employee = Employee.query.get(id)
    # if not found
    if specific_employee is None:
        result = {"message": "employee not found"}
        return jsonify(result), 404
    try:
        # update all values in "specific_employee" with values from "update_data" dictionary
        # loop request body data (update_data) as you only want to work with the specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change our db which is unsafe!!!!
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_employee, key):
                # update the value of that key
                setattr(specific_employee, key, value)
                # commit changes after all keys have been updated
        db.session.commit()
        # check if employee was correctly updated
        # print(specific_employee)
        result = {
            "messsage": "employee successfully updated",
            "data": specific_employee.to_dict(),
        }
        return jsonify(result)
    # if an error occured while updating
    except Exception as e:
        db.session.rollback()  # undo the changes (unless they have already been committed)
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500


# Delete the specific employee from azure db request
@employees_bp.delete("/<id>")
def delete_employee(id):
    # get specific employee from "id" in URL
    employee_del = Employee.query.get(id)
    # if we did not find it
    if not employee_del:
        result = {"message": "employee not found"}
        return jsonify(result), 404
    try:
        # delete from database
        db.session.delete(employee_del)
        # making the change permanent
        db.session.commit()
        result = {
            "messsage": "employee successfully deleted",
            "data": employee_del.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"An error occured:": str(e)}
        return jsonify(result), 500
