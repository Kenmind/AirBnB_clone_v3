#!/usr/bin/python3
""" route for handling City objects and operations
"""

from api.v1.views import app_views, storage
from flask import jsonify, request, abort
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_city_by_state(state_id):
    """ Retrieves a list of all City objects of a State
        if state_id has no link, raise 404 error
        returns: json of all cities
    """
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)

    city_list = []

    for obj in state_obj.cities:
        city_list.append(obj.to_dict())

    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves a City object
        if city_id not found raise a 404 error
    """
    city_obj = storage.get("City", str(city_id))

    if city_obj is None:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """ Deletes a City object
        if city_id not found raise a 404 error
        returns: empty dict with 200 status code
    """
    city_obj = storage.get("City", str(city_id))

    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()

    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a City
        if state_id is not linked to any State raise 404 a error.
        if HTTP body request is not valid JSON.
        raise a 404 error
        if dict has no key name, raise 400 error
        :returns: new City with status code 201
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, "Not a JSON")

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, "Missing name")

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object
        if city_id not found, raise a 404 error
        Update the City obj with all key-value pairs of the dictionary.
        ignore keys: id, created_at, updated_at
        :returns the City object with status code 200
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, "Not a JSON")
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)
    for k, v in city_json.items():
        if k not in ["id", "created_at", "update_at"]:
            setattr(city_obj, k, v)
    city_obj.save()

    return jsonify(city_obj.to_dict())
