#!/usr/bin/python3
""" Flask app """

from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint, make_response
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """ Teardown method """
    storage.close()


@app.errorhandler(404)
def hande_404_error(error):
    """ handles the 404 error
        returns 404 json
    """
    data = {"error": "Not found"}

    return make_response(jsonify(data), 404)


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")))
