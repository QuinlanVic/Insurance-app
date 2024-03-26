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