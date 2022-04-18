#!/usr/bin/python3
""" route for handling Place and Amenity objects default RESTfule API actions.
"""

from api.v1.views import app_views, storage
from flask import abort, jsonify
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_place(place_id):
    """ Retrieves a list of all Amenity objects of a Place
        if place_id has no link, raise a 404 error
        returns: json of all amenities
    """
    place_obj = storage.get("Place", str(place_id))

    amenities_list = []

    if place_obj is None:
        abort(404)

    for obj in place_obj.amenities:
        amenities_list.append(obj.to_dict())

    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/amenity_id",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """ Deletes a Amenity object to a place
        if place_id is not linked to a place raise 404 error
        if amenity_id is not linked to any amenity raise a 404 error
        if the Amenity is not linked to the Place before the request,
        raise a 404 error.
        returns: empty dict with 200 status code
    """
    place_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    found_amenity = 0

    if not place_obj or not amenity_obj:
        abort(404)

    for obj in place_obj.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                place_obj.amenities.remove(obj)
            else:
                place_obj.amenity_ids.remove(obj.id)
            place_obj.save()
            found_amenity = 1
            break
    if found_amenity == 0:
        abort(404)
    else:
        res = jsonify({})
        res.status_code = 201
        return res


@app_views.route("/places/<place_id>/amenities/amenity_id",
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """ Links a Amenity object to a Place
        if place_id is not linked to any place raise a 404 error.
        if amenity_id is not linked to any Amenity veofre the request,
        raise a 404 error.
        raise a 404 error
        if the Amenity is already linked to the place,
            return the Amenity wit status code 200
        :returns: the Amenity with status code 201
    """
    place_obj = storage.get("Place", str(place_id))
    amenity_obj = storage.get("Amenity", str(amenity_id))
    found = None

    if not place_obj or not amenity_obj:
        abort(404)

    for obj in place_obj.amenities:
        if str(obj.id) == amenity_id:
            found = obj
            break
    if found is not None:
        return jsonify(found.to_dict())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place_obj.amenities.append(amenity_obj)
    else:
        place_obj.amenities = amenity_obj

    place_obj.save()

    response = jsonify(amenity_obj.to_dict())
    response.status_code = 201

    return response
