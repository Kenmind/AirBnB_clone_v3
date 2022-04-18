#!/usr/bin/python3
""" route for handling User objects and operations
"""

from api.v1.views import app_views, storage
from flask import jsonify, request, abort
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves a list of all User objects
        returns: json of all users
    """
    user_list = []
    user_obj = storage.all("User")
    for obj in user_obj.values():
        user_list.append(obj.to_dict())

    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves a User object
        if user_id not found raise a 404 error
    """
    user_obj = storage.get("User", str(user_id))

    if user_obj is None:
        abort(404)

    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object
        if user_id is not found raise a 404 error
    """
    user_obj = storage.get("User", str(user_id))

    if user_obj is None:
        abort(404)

    storage.delete(user_obj)
    storage.save()

    return jsonify({})


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a new User
        if HTTP body request is not valid JSON
        raise a 404 error
        if dict has no key name, raise 400 error
        :returns: new the User with status code 201
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, "Not a JSON")
    if "name" not in user_json:
        abort(400, "Missing name")

    new_user = User(**user_json)
    new_user.save()
    resp = jsonify(new_user.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object
        if user_id not found, raise a 404 error
        update User obj with all key-value pairs of the dictionary
        ignore keys: id, created_At and updated_ap
        :returns the User object with status code 200
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, "Not a JSON")
    user_obj = storage.get("User", str(user_id))
    if user_obj is None:
        abort(404)
    for k, v in user_json.items():
        if k not in ["id", "created_at", "update_at"]:
            setattr(user_obj, k, v)
    user_obj.save()

    return jsonify(user_obj.to_dict())
