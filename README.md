# Welcome to CoolWater 
## A car insurance app that provides users with a comfortable way to be in charge of their future

## Application structure
## Routing 


## Files
Models folder
- Consists of all classes that represent table schemas

Routes folder
- Consists of blueprints defining the routes for navigaiton through the application
- Inner routes folder
    - Consists of all API calls for CRUD operations (largely for front-end developers to use)

Static folder
- Consists of most (almost all) the CSS code for the project

Templates folder
- Consists of all HTML files used to represent web pages of the application

app.py file
- Links all of the functionalities to create the application
    - connects to database and links all routes for navigation

DockerFile
- consists of the code to deploy the applicaiton to render.com

localdata.py
- consists of dummy dicitonary data that is put into the tables of the database connected to the application

requirements.txt
- consists of the list of required packages and verisons (project dependencies)

extensions.py
- consists of code/variables/data that is required globally in the application

Project Report
- Consists of a summary of the developer's experience and some more information regarding the application

RESTful API Documentation
- Consists of structure of API calls for the applicaiton and what they do

High-level Overview of Developer's Experience
- Implemented the functionality that we learned in class for this application throughout the course
- Worked through any errors with trial and error/thorough debugging with techniques learnt throughout my career and specific techniques from the course



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
Useful for saving all specific packages in case my environment is deleted for example

### Install add dependencies from requirements.txt
```sh
pip install -r requirements.txt
```