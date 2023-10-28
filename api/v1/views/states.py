#!/usr/bin/python3
"""Defines the modules"""
from api.v1.views import app_views
from models import storage
from flask import abort


@app_views.route('/states', methods=['GET'])
def get_states():
    """retrieves an object into a valid json"""
    st = storage.all("States")
    states_dict = st.to_dict()
    return states_dict


@app_views.route('/states/<state_id>', methods=['GET'])
def useid(state_id):
    """retrieve a specific state using its id"""

    st = storage.all("State")
    if st['id'] == state_id:
        states_dict = st.to_dict()
        return states_dict
    else:
        abort(404)
