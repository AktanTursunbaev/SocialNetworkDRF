# SocialNetworkDRF

## Project Setup

Install required packages:

`pip3 install -r requirements.txt`
 
Initialize database:

`python3 manage.py migrate`

Creating superuser:

`python3 manage.py createsuperuser`

Running the server:

`python3 manage.py runserver`

_Run last three commands from project directory (SocialNetworkDRF folder)_

---

## API Testing Bot Usage

This bot is just a python script that populates project database with users, posts and likes

To edit configurations for this bot, open config.py located in api\_test_bot directory and replace currently set values to your values

Before running this bot, make sure that you have api server running and you are located in api\_test_bot directory. To run this bot, just run main.py as a simple python file (`python3 main.py`)

## API Documentation

To view API documentation, run server and visit http://127.0.0.1:8000/docs/

