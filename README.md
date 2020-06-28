# Flask Shows 

This project parse an excel of shows titles and get their directors, save it to the database, and finally generate pdf of all the availabe shows 
## Requirements
  - Python3
  - Mysql

## Excel Sample
  - Excel should contain one column with the following titles
  -- movie
  -- series
  -- episode
these are the shows type that this project can handle

## Installation
    - pip install -e .
    - flask ini-db
    - flask run # for localhost

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