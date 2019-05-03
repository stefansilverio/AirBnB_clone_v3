#!/usr/bin/python3
"""Flask module to configure routes for place class api calls"""
from models.place import Place
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from os import getenv


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False,
                 methods=['GET'])
def places_get_all(city_id):
    """Handle GET request for places"""
    cityGet = storage.get("City", city_id)
    if cityGet is None:
        abort(404)
    return jsonify([place.to_dict() for place in cityGet.places])


@app_views.route("/places/<place_id>")
def places_get_one(place_id):
    """retreive one place obj"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def place_delete(place_id):
    """Handles DELETE request with place objects"""
    place_obj = storage.get("Place", place_id)
    if place_obj is not None:
        storage.delete(place_obj)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False, methods=['POST'])
def place_post(city_id):
    """Handles POST request with place objects"""
    user_data = request.get_json()
    if user_data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in user_data.keys():
        abort(400, 'Missing user_id')
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        abort(404)
    new_place = Place(**(user_data))
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def place_put(place_id):
    """Handles PUT request with place object"""
    user_data = request.get_json()
    if user_data is None:
        abort(400, 'Not a JSON')
    all_places = storage.all("Place").values()
    if place_id not in all_places:
        abort(404)
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    for k, v in user_data.items():
        if k is not ["id", "created_at", "updated_at"]:
            setattr(place_obj, k, v)
    place_obj.save()
    return jsonify(place_obj.to_dict())
