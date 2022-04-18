#!/usr/bin/python3
""" route for handling State objects and operations
"""

from api.v1.views import app_views, storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_all_state():
    """ Retrieves a list of all state objects
        returns: json of all States
    """
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_dict())

    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieves a State object
        if state id not found raise a 404 error
    """
    fetch_obj = storage.get("State", str(state_id))

    if fetch_obj is None:
        abort(404)

    return jsonify(fetch_obj.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """ Deletes a state object
        if state id not found raise a 404 error
    """
    fetch_obj = storage.get("State", str(state_id))

    if fetch_obj is None:
        abort(404)

    storage.delete(fetch_obj)
    storage.save()

    return jsonify({})


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State
        if HTTP body request is not valid JSON
        raise a 404 error
        if dict has no key name, raise 400 error
        :returns: new State with status code 201
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, "Not a JSON")
    if "name" not in state_json:
        abort(400, "Missing name")

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object
        if state_id not found, raise a 404 error
        update State obj with all key-value pairs of the dictionary
        ignore keys: id, created_At and updated_ap
        :returns the State object with status code 200
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, "Not a JSON")
    fetch_obj = storage.get("State", str(state_id))
    if fetch_obj is None:
        abort(404)
    for k, v in state_json.items():
        if k not in ["id", "created_at", "update_at"]:
            setattr(fetch_obj, k, v)
    fetch_obj.save()

    return jsonify(fetch_obj.to_dict())
