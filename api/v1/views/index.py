#!/usr/bin/python3
"""Defines the modules"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status')
def return_json():
    """return a json object"""

    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def count():
    """retrieves the number of each objects by type"""

    res = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(res)
