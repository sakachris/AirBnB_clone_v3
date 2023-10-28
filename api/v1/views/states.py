#!/usr/bin/python3
"""Defines the modules"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify

@app_views.route('/states', methods=['GET'])
def get():
    """retrieve all the state objects"""
    st = storage.all("State")

    all_states = [] # empty basket
    for state in st.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)
