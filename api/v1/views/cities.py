#!/usr/bin/python3
""" module for city api """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """ gets all city objects per state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """ gets city object per id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_city(city_id):
    """ deletes a city object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def add_city(state_id):
    """ adds new city """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    if 'name' not in js_data:
        # abort(400, 'Missing name')
        return jsonify({"error": "Missing name"}), 400
    js_data['state_id'] = state_id
    city = City(**js_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ updates a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    for key, val in js_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
