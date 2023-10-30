#!/usr/bin/python3
""" module for review api """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def amenities(place_id):
    """ gets all amenity objects per place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amenities(place_id, amenity_id):
    """ deletes an amenity object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not place.amenities:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_review(place_id, amenity_id):
    """link amenity to place"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)

    if places.amenities:
        return jsonify(amenities.to_dict()), 200
    places = Place(**amenities)
    places.save()
    return jsonify(places.to_dict()), 201
