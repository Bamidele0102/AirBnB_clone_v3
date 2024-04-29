#!/usr/bin/python3
"""
Creates a route /status on the object app_views
that returns a JSON: "status": "OK"
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns API status."""
    return jsonify({"status": "OK"})
