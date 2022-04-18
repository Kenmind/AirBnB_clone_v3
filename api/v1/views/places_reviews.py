#!/usr/bin/python3
""" route for handling Review objects and operations
"""

from api.v1.views import app_views, storage
from flask import jsonify, request, abort
from models.review import Review


@app_views.route("/places/<place_id>/review", methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    """ Retrieves a list of all Review objects of any Place
        if place_id has no link, raise a 404 error
        returns: json of all reviews
    """
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)

    review_list = []

    for obj in place_obj.reviews:
        review_list.append(obj.to_dict())

    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """ Retrieves a Review object
        if reviw_id is not found raise a 404 error
    """
    review_obj = storage.get("Review", str(review_id))

    if review_obj is None:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object
        if review_id is not found raise a 404 error
        returns: empty dict with 200 status code
    """
    review_obj = storage.get("Review", str(review_id))

    if review_obj is None:
        abort(404)

    storage.delete(review_obj)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_a_review(place_id):
    """ Creates a new Review
        if place_id is not linked to any place raise a 404 error.
        if HTTP body request is not valid JSON.
        raise a 404 error
        if dict has no key name, raise 400 error
        :returns: the new Review with status code 201
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


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object
        if review_id is not found, raise a 404 error
        Update the Review obj with all key-value pairs of the dictionary.
        ignore keys: id, created_at, updated_at
        :returns the Review object with status code 200
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, "Not a JSON")
    review_obj = storage.get("Review", str(review_id))
    if review_obj is None:
        abort(404)
    for k, v in review_json.items():
        if k not in ["id", "created_at", "update_at"]:
            setattr(review_obj, k, v)
    review_obj.save()

    return jsonify(review_obj.to_dict())
