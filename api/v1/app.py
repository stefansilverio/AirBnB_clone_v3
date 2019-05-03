#!/usr/bin/python3
"""Py module utilizes flask to run app"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(invalid_path):
    """Error handling function for 404 page"""
    return jsonify(error="Not found"), 404


@app.teardown_appcontext
def tearDown(error):
    """tearDown method"""
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'), port=int(getenv('HBNB_API_PORT')),
            threaded=True)
