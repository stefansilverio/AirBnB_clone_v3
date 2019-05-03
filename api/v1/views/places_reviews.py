#!/usr/bin/python3
"""holds class Review"""
from models.review import Review
from flask import abort
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, request
from os import getenv
from models import storage
import json


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['GET'])
def all_reviews(place_id):
    """grab all reviews of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['GET'])
def get_review_obj(review_id):
    """retrieve Review obj"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """delete a Review"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """create new Review obj"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    if 'text' not in data.keys():
        abort(400, "Missing text")
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    new_review = Review(**data)
    setattr(new_review, 'place_id', place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """update Review object: idempotent"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    review = storage.get("Review", review_id)
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
