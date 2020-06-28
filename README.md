# Flask Shows 

This project parse an excel of shows titles and get their directors, save it to the database, and finally generate pdf of all the availabe shows 
## Requirements
  - Python3
  - Mysql
  - sudo apt-get install libmariadb-dev

## Excel Sample
  - Excel should contain one column with the following titles
  -- movie
  -- series
  -- episode
these are the shows type that this project can handle

## Installation
    - pip install -e .
    # set the enviroment https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
    # Create a database
    # Go to flask/db.py and change mariadb connect params
    # Go to __init__.py and set your db credentials in this variable SQLALCHEMY_DATABASE_URI
    # run init-db to fresh migrate the schema
    - flask init-db
    # set FLASK_APP=flaskr, set FLASK_ENV=development, set FLASK_DEBUG=1
    - flask run # for localhost
NOTE: if you are using Linux or max go to flaskr/db.py and replace double '\\\\' backslashes by slash '/'
## Available APIs
    # movie is a variable this API returns list of shows and their directors
    # parameter: movie|series|episode, offset, limit
    # method: GET
    - api/shows/movie?offset=0&limit=10
    # Upload excel to import
    # parameter: .xlsx file
    # method: POST
    - api/excel/upload
    # generate and returns generated PDF path
    # method: get
    - api/shows/pdf-export