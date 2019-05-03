#!/usr/bin/python3
"""Flask module to configure routes for state class api calls"""
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from os import getenv


@app_views.route("/amenities",
                 defaults={"amenity_id": None},
                 strict_slashes=False,
                 methods=['GET'])
@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['GET'])
def amenity_get(amenity_id):
    """Handle GET request for amenities"""
    amenities = storage.all("Amenity").values()
    if amenity_id is None:  # grab all amenities
        return jsonify(
            [amenity.to_dict() for amenity in amenities]
        )
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is not None:
        return jsonify(amenity_obj.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def amenity_delete(amenity_id):
    """Handles DELETE request with amenity objects"""
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is not None:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def amenity_post():
    """Handles POST request with amenity objects"""
    user_data = request.get_json()
    if user_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in user_data.keys():
        abort(400, 'Missing name')
    new_amenity = Amenity(**(user_data))
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def amenity_put(amenity_id):
    """Handles PUT request with amenity object with amenity id"""
    user_data = request.get_json()
    if user_data is None:
        abort(400, 'Not a JSON')
    amenity_obj = storage.get("Amenity", amenity_id)
    if amenity_obj is None:
        abort(404)
    for k, v in user_data.items():
        if k is not ["id", "created_at", "updated_at"]:
            print(type(amenity_obj))
            setattr(amenity_obj, k, v)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict())
