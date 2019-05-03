#!/usr/bin/python3
"""Flask module to configure routes for state class api calls"""
from models.state import State
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from os import getenv


@app_views.route("/states",
                 defaults={"state_id": None},
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['GET'])
def state_get(state_id):
    """Handle GET request for states"""
    states = storage.all("State")
    stateGet = storage.get("State", state_id)
    if state_id is None:
        return jsonify(
            [state.to_dict() for state in states.values()]
        )
    elif stateGet is not None:
        return jsonify(
            stateGet.to_dict()
        )
    else:
        abort(404)


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def state_delete(state_id):
    """Handles DELETE request with state objects"""
    stateGet = storage.get("State", state_id)
    if stateGet is not None:
        storage.delete(stateGet)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states",
                 strict_slashes=False,
                 methods=['POST'])
def state_post():
    """Handles POST request with state objects"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
        abort(400, 'Missing name')
    new_state = State(**(data))
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def state_put(state_id):
    """Handles PUT request with state object with state id"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    stateGet = storage.get("State", state_id)
    if stateGet is None:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(stateGet, k, v)
    stateGet.save()
    return jsonify(stateGet.to_dict())
