#!/usr/bin/python3
""" Flask app """

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """ Teardown method """
    storage.close()


@app.errorhandler(404)
def hande_404_error(exception):
    """ handles the 404 error
        returns 404 json
    """

    data = {
            "error": "Not Found"
            }

    res = jsonify(data)
    res.status_code = 404

    return (res)


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_PORT"))
