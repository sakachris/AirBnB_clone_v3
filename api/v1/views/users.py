#!/usr/bin/python3
""" module for user api """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_users(user_id=None):
    """ gets all user objects """
    if user_id is None:
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])
    else:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_user(user_id):
    """ deletes a user object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return (jsonify({})), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def add_user():
    """ adds new user """
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    if 'email' not in js_data:
        # abort(400, 'Missing name')
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in js_data:
        # abort(400, 'Missing name')
        return jsonify({"error": "Missing password"}), 400
    user = User(**js_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ updates a user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    js_data = request.get_json()
    if not js_data:
        abort(400, 'Not a JSON')
    for key, val in js_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
