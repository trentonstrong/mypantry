from uuid import uuid4 as uuid
try:
    from json import dumps
except ImportError:
    from simplejson import dumps

from flask import Flask, Response
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from sqlalchemy.sql.functions import now

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


def jsonify(f):
    def inner(*args, **kwargs):
        return Response(dumps(f(*args, **kwargs)), mimetype='application/json')
    return inner


class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    token = db.Column(db.String(255), unique=True)


class Meal(db.Model):

    (BREAKFAST, AM_SNACK, LUNCH, PM_SNACK, DINNER, EXTRA_SNACK) = (0, 1, 2, 3, 4, 5)

    id = db.Column(db.Integer, primary_key=True)

    meal_time = db.Column(db.Integer, nullable=False)

    data = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=now())

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Meal, methods=['GET', 'POST', 'DELETE'])

db.create_all()

@app.route('/api/authenticate')
@jsonify
def authenticate():
    token = str(uuid())
    new_device = Device(token=token)
    db.session.add(new_device)
    db.session.commit()
    return {"token": token}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
