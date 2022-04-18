#!/usr/bin/python3
""" route for handling Amenity objects and operations
"""

from api.v1.views import app_views, storage
from flask import jsonify, request, abort
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_all_amenity():
    """ Retrieves a list of all Amenitty objects
        returns: json of all Amenities
    """
    amenity_list = []
    amenity_obj = storage.all("Amenity")
    for obj in amenity_obj.values():
        amenity_list.append(obj.to_dict())

    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves an Amenity object
        if state id not found raise a 404 error
    """
    amenity_obj = storage.get("Amenity", str(amenity_id))

    if amenity_obj is None:
        abort(404)

    return jsonify(amenity_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object
        if state id not found raise a 404 error
        returns: an empty dictionary with status code 200
    """
    amenity_obj = storage.get("Amenity", str(amenity_id))

    if amenity_obj is None:
        abort(404)

    storage.delete(amenity_obj)
    storage.save()

    return jsonify({})


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates a Amenity
        if HTTP body request is not valid JSON
        raise a 404 error
        if dict has no key name, raise 400 error
        :returns: new Amenity with status code 201
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, "Not a JSON")
    if "name" not in amenity_json:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    resp = jsonify(new_amenity.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a Amenity object
        if the amenity_id is not found, raise a 404 error
        update Amenity obj with all key-value pairs of the dictionary
        ignore keys: id, created_At and updated_ap
        :returns the Amenity object with status code 200
    """
    amenity_json = request.get_json(silent=True)
    if amenity_json is None:
        abort(400, "Not a JSON")
    amenity_obj = storage.get("Amenity", str(amenity_id))
    if amenity_obj is None:
        abort(404)
    for k, v in amenity_json.items():
        if k not in ["id", "created_at", "update_at"]:
            setattr(amenity_obj, k, v)
    amenity_obj.save()

    return jsonify(amenity_obj.to_dict())
