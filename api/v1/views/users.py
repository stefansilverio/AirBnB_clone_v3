#!/usr/bin/python3
"""Flask module to configure routes for User class api calls"""
from models.user import User
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from os import getenv


@app_views.route("/users",
                 defaults={"user_id": None},
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['GET'])
def user_get(user_id):
    """Handle GET request for users"""
    users = storage.all("User")
    userGet = storage.get("User", user_id)
    if user_id is None:
        return jsonify(
            [user.to_dict() for user in users.values()]
        )
    elif userGet is not None:
        return jsonify(
            userGet.to_dict()
        )
    else:
        abort(404)


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def user_delete(user_id):
    """Handles DELETE request with User objects"""
    userGet = storage.get("User", user_id)
    if userGet is not None:
        storage.delete(userGet)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users",
                 strict_slashes=False,
                 methods=['POST'])
def user_post():
    """Handles POST request with User objects"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data.keys():
        abort(400, 'Missing email')
    if 'password' not in data.keys():
        abort(400, 'Missing password')
    new_user = User(**(data))
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def user_put(user_id):
    """Handles PUT request with User object with user id"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    userGet = storage.get("User", user_id)
    if userGet is None:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(userGet, k, v)
    userGet.save()
    return jsonify(userGet.to_dict())
