#!/usr/bin/python3
""" route for handling Place and Amenity objects default RESTfule API actions.
"""

from api.v1.views import app_views, storage
from flask import abort, jsonify


@app_views.route("/places/<place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_place(place_id):
    """ Retrieves a list of all Amenity objects of a Place
        if place_id has no link, raise a 404 error
        returns: json of all amenities
    """
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)

    review_list = []

    for obj in place_obj.reviews:
        review_list.append(obj.to_dict())

    return jsonify(review_list)


@app_views.route("/places/<place_id>/amenities/amenity_id",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """ Deletes a Amenity object to a place
        if place_id is not linked to a place raise 404 error
        if amenity_id is not linked to any amenity raise a 404 error
        if the Amenity is not linked to the Place before the request,
        raise a 404 error.
        returns: empty dict with 200 status code
    """
    review_obj = storage.get("Review", str(review_id))

    if review_obj is None:
        abort(404)

    storage.delete(review_obj)
    storage.save()

    return jsonify({})


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
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, "Not a JSON")

    if not storage.get("Place", str(place_id)):
        abort(404)

    if "name" not in review_json:
        abort(400, "Missing name")

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    resp = jsonify(new_review.to_dict())
    resp.status_code = 201

    return resp
