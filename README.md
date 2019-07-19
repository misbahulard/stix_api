# stix_api
STIX api using Flask - python 2.7

## Create python virtual environment
```
virtualenv venv
```

## Install dependencies
```
pip install -r requirements.txt
```

## Run app
### Easy
for easy run, run the batch script `env.bat` or `sh env.sh`

### Manual
set the environment variable and run the app
```
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```