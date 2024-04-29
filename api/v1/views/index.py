#!/usr/bin/python3
"""
Creates a route /status on the object app_views
that returns a JSON: "status": "OK"
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns API status."""
    return jsonify({"status": "OK"})


# Create an endpoint that retrieves the number of each objects by type:
@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each object type"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
