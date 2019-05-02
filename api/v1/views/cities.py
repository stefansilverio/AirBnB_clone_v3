#!/usr/bin/python3
"""holds class City"""
from models.state import State
from models.city import City
from flask import abort
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, request
from os import getenv
from models import storage
import json


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['GET'])
def all_cities(state_id):
    """grab all cities in a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = storage.all("City").values()
    obj = [city.to_dict() for city in cities if city.state_id == state_id]
    return jsonify(obj)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def get_city_obj(city_id):
    """retrieve city obj"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """create new city obj"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(400, "Missing name")
    new_city = City(**data)
    setattr(new_city, 'state_id', state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    """create or update: idempotent"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(400, "Missing name")
    city = storage.get(City, city_id)
    for k, v in data.items():
        if k != "id" and k != "created_at"\
           and k != "updated_at" and k != "state_id":
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
