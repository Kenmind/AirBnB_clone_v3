#!/usr/bin/python3
""" Index"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route("/status", strict_slashes=False)
def status():
    """ status route
        :return: json response
    """
<<<<<<< HEAD
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200
=======
    data = {"status": "OK"}

    res = jsonify(data)
>>>>>>> 393c1feee075498392811f7b90a27c4f82cef5fa

    return resp


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ retrives the number of objects by type"""
    ret_dict = {}

    data = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User"),
            }

    for key, value in data.items():
        ret_dict[key] = storage.count(value)
    return jsonify(ret_dict)


if __name__ == "__main__":
    pass
