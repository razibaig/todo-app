# Todo Flask Application

## Setting up project (dev env)

### Pre-requisites:
- Flask (install flask: ```pip install Flask```)
- Flask-SQLAlchemy (install flask-sqlalchemy: ```pip install Flask-SQLAlchemy```)
- Flask-HTTPAuth (install Flask-HTTPAuth: ```pip install flask-httpauth```)
- Flask-RESTful (install Flask-RESTful: ```pip install flask-restful```)

### Running the Flask application:
- After cloning the repo, cd into the directory with the ```app.py``` file.
- Create a secrets.json file with the following format:
```
  {
      "user":  "username_of_your_choice",
      "pass": "password_of_your_choice"
  }
```
- These credentials will be required for the Basic Authentication required to access the endpoints.

- Start the flask application using the following command:
```
    python app.py
``` 