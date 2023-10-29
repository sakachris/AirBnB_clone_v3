#!/usr/bin/python3
""" module for state api """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_states(state_id=None):
    """ gets all state objects """
    if state_id is None:
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id):
    """ deletes a state object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def add_state():
    """ adds new state """
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    if 'name' not in js_data:
        # abort(400, 'Missing name')
        return jsonify({"error": "Missing name"}), 400
    state = State(**js_data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ updates a state """
    state = storage.get(State, state_id)
    if not state:
        abort(400)
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    for key, val in js_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
