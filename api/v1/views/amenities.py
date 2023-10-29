#!/usr/bin/python3
""" module for amenity api """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenities(amenity_id=None):
    """ gets all amenity objects """
    if amenity_id is None:
        amenities = storage.all(Amenity).values()
        return jsonify([amenity.to_dict() for amenity in amenities])
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id):
    """ deletes a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def add_amenity():
    """ adds new amenity """
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    if 'name' not in js_data:
        # abort(400, 'Missing name')
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**js_data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """ updates a amenity """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    for key, val in js_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
