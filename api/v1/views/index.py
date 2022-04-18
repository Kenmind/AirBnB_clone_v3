#!/usr/bin/python3
""" Index"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ status route
        :return: json response
    """
    data = {
            "status": "OK"
    }

    res = jsonify(data)
    res.status_code = 200

    return res


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """ retrives the number of objects by type"""
    data = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User"),
            }

    res = jsonify(data)
    res.status_code = 200

    return res
