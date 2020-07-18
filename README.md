# Bottles

Microblog app project derived from [the official Flask tutorial](http://flask.pocoo.org/docs/1.0/tutorial/).

## Setup
Before using app for development purposes you need to install it:
````
pip install -e .
````

Before running a server you need to provide enviroment variable either by setting them up manually or using .env file:
```
FLASK_APP=bottles
FLASK_ENV=development
DATABASE_URI=postgresql://your_database
SECRET_KEY=your_key
```

Before the first launch you need to setup database:
````
flask init_db
````

If reset of the database is needed, you can use (this will delete all the stored data!):
````
flask reset_db
````

## Run server
To run Bottles dev-server execute:
````
flask run
````

## Tests
To run the tests execute:
````
coverage run -m pytest
````

For report:
````
coverage html
````
