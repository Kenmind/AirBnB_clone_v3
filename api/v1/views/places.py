#!/usr/bin/python3
""" route for handling Place objects and operations
"""

from api.v1.views import app_views, storage
from flask import jsonify, request, abort
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_place_by_city(city_id):
    """ Retrieves a list of all Place objects of any City
        if city_id has no link, raise a 404 error
        returns: json of all places
    """
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)

    place_list = []

    for obj in city_obj.places:
        place_list.append(obj.to_dict())

    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """ Retrieves a Place object
        if place_id is not found raise a 404 error
    """
    place_obj = storage.get("Place", str(place_id))

    if place_obj is None:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object
        if place_id is not found raise a 404 error
        returns: empty dict with 200 status code
    """
    place_obj = storage.get("Place", str(place_id))

    if place_obj is None:
        abort(404)

    storage.delete(place_obj)
    storage.save()

    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_a_place(city_id):
    """ Creates a new Place
        if city_id is not linked to any city raise a 404 error.
        if HTTP body request is not valid JSON.
        raise a 404 error
        if dict has no key name, raise 400 error
        :returns: the new Place with status code 201
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, "Not a JSON")

    if not storage.get("City", str(city_id)):
        abort(404)

    if "name" not in place_json:
        abort(400, "Missing name")

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object
        if place_id is not found, raise a 404 error
        Update the Place obj with all key-value pairs of the dictionary.
        ignore keys: id, created_at, updated_at
        :returns the Place object with status code 200
    """
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, "Not a JSON")
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    for k, v in place_json.items():
        if k not in ["id", "created_at", "update_at"]:
            setattr(place_obj, k, v)
    place_obj.save()

    return jsonify(place_obj.to_dict())
