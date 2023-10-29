#!/usr/bin/python3
"""
module for api index page
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ returns json string """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def obj_count():
    """ returns number of objects per class """
    obj_dict = {
                "amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": storage.count("State"),
                "users": storage.count("User")
                }
    return jsonify(obj_dict)
