#!/usr/bin/python3
"""Define the modules"""
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error(err):
    """format the 4040 error return message"""

    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def clean_up(exception):
    """perform cleanup after a request has been processed"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True)
