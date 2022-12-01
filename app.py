"""
Main flask project file.
"""
import json
import logging
import os
from http import HTTPStatus

from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, make_response, jsonify

app = Flask(__name__)
auth = HTTPBasicAuth()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def load_credentials(secret_path):
    """Loads the secret credentials from the specified file.
    : param secret_path: path to the file containing the secret credentials
    :returns: a tuple of the form (username, password)
    """
    if not secret_path:
        data = json.loads(os.environ['SECRET_PATH'])
    else:
        try:
            with open(secret_path, encoding='utf-8') as data_file:
                data = json.load(data_file)
        except EnvironmentError:
            logging.error("No secrets.json file found")
            raise
    try:
        username = data['user']
        password = data['pass']
    except KeyError:
        logging.error(
            "File does not contain credentials in the expected format."
        )
        raise
    return {username: generate_password_hash(password)}


users = load_credentials("secrets.json")


@auth.verify_password
def verify_password(username, password):
    """Method to verify password."""
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


class Todo(db.Model):
    """Todos object model class."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.String(255))
    is_complete = db.Column(db.Boolean)

    def serialize(self):
        """Serializing the todos object."""
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "is_complete": self.is_complete,
        }


@app.route('/')
@auth.login_required
def todo_list_page():
    todo_objects = Todo.query.all()
    return render_template("base.html", todo_list=todo_objects)


@app.route('/list')
@auth.login_required
def todo_list():
    """Endpoint to get list of todos"""
    todo_objs = Todo.query.all()
    todo_json = [obj.serialize() for obj in todo_objs]

    return make_response(jsonify(todo_json)), HTTPStatus.OK


@app.route("/add", methods=["POST"])
@auth.login_required
def add():
    """Add todos endpoint"""
    request_data = request.get_json()
    title = request_data.get("title")
    text = request_data.get("text")
    new_todo = Todo(title=title, text=text, is_complete=False)
    db.session.add(new_todo)
    db.session.commit()

    return make_response(jsonify(new_todo.serialize())), HTTPStatus.CREATED


@app.route("/update/<int:todo_id>", methods=["POST"])
@auth.login_required
def update(todo_id):
    """Update todos endpoint."""
    request_data = request.get_json()
    title = request_data.get("title")
    text = request_data.get("text")
    is_complete = request_data.get("is_complete")
    todo = Todo.query.filter_by(id=todo_id).first()
    if title:
        todo.title = title
    if text:
        todo.text = text
    if is_complete:
        todo.is_complete = is_complete
    db.session.commit()
    return make_response(jsonify(todo.serialize())), HTTPStatus.OK


@app.route("/delete/<int:todo_id>", methods=["DELETE"])
@auth.login_required
def delete(todo_id):
    """Delete endpoint."""
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return make_response(jsonify(todo.serialize())), HTTPStatus.OK


if __name__ == "__main__":
    """Main function."""
    with app.app_context():
        db.create_all()
    app.run(debug=True)
