# Welcome to CoolWater💧
## A car insurance application that provides users with a comfortable way to stay in charge of their financial future with us

## Benefits/Purpose of the Web Application
It allows clients to read through the articles, policies and background information of the company. In addition, it offers them a way to contact the company. Lastly, and most importantly it allows users to calculate car insurance quotes and manage their policies and claims after logging in through a secure portal.
The admin view allows the admin user to manipulate all of the application's data through CRUD operations.

## Application structure
A logged out user has access to all pages except the "Profile", "My Policies", "My Claims" and "Make a Claim" pages. They can browse all other pages and are able to calculate car insurance quotes. To access more functionality they have to login or register/sign up. 

After logging in, they can access their profile, policies and claims as well as take out new or delete existing policies and claims. Users also have the ability to terminate their accounts. A new "update profile" functionality is currently in the works.

Additionally there is an "admin" view which is the same as a logged in users view except they can update, create and delete all application data i.e., articles, policies, users, claims and employees (some CRUD operations are still to be implemented).


## Routing 
Each file has an associated route that is defined in modular blueprints. These blueprints are loaded into the "app.py" file which manages and links the entire functionality of the application together. 

## File Structure
Models folder
- Consists of all classes that represent table schemas

Routes folder
- Consists of blueprints defining the routes for navigation through the application
- Inner routes folder - json
    - Consists of all API calls for CRUD operations (largely for front-end developers to use)
        - (some calls are yet to be implemented)

Static folder
- Consists of all the CSS code for the project in the "styles.css" file

Templates folder
- Consists of all HTML files used to represent web pages of the application

app.py file
- Links and manages all of the functionalities of the application
    - i.e., connects to the database and links all HTML files representing web pages and routes for navigation

DockerFile
- consists of the code to deploy the application to "render.com"

localdata.py
- consists of dummy dicitonary data that is put into the tables of the database connected to the application
    - is very useful for creating POSTMAN API calls to insert data into the database extremely easily

requirements.txt
- consists of the list of required packages and their versions (project dependencies)

extensions.py
- consists of code/variables/data that is required globally in the application

Project Report
- Consists of a summary of the developer's experience and some more information regarding the application (was created at the start of the project and abandoned to create this "README" file instead)

## POSTMAN Collection
The JSON file with all POSTMAN requests can be found in the "Insurance App.postman_collection.json" document 

## Connection to Local/Azure Database 
Restricted access, have to ask for confidential information.

# Setup

## Virtual Environment
```bash
python -m venv myenv
```

## Activate Environment
(powershell)
```sh
.\myenv\Scripts\Activate.ps1 
```

## Git
### Initialise Repository
```bash
git init
```
### Git Ignore
Create `.gitignore` file and add "myenv" to stop tracking that folder's changes

### Add files
1. Stage files -> 
```bash
git add .
```
2. Commit files ->
```bash
git commit -m "message"
```
3. Push to GitHub 

## Installing Flask
1. Ensure that your "env" is activated - [Guide](https://flask.palletsprojects.com/en/3.0.x/installation/#python-version)
2. Pip Install Flask ->
```sh
pip install Flask
```

# Why Flask?
Micro-framework, increased freedom, lightweight, tools for REST API implementation, improved developer's experience

# How to run Flask
```sh
flask --app main run
```

-> Only if file name is `app.py`
```sh
flask run
```

-> Pass in `debug` flag to go into development mode
```sh
flask run --debug
```


## Dependencies
### Take snapshots of all project packages (have to update with each new package installation)
```sh
pip freeze > requirements.txt
```
Useful for saving all specific packages in case your environment is deleted for example

### Install all dependencies from "requirements.txt"
```sh
pip install -r requirements.txt
```

