#!/usr/bin/python3
""" Index"""

from flask import jsonify
from api.v1.views import app_views


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
