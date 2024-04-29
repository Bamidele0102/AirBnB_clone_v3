#!/usr/bin/python3
"""
Creating a Flask app; and registering blueprint (app_views)
to the Flask instance app.
"""
# Import necessary modules
from flask import Flask, jsonify  # Import jsonify from flask
from api.v1.views import app_views  # Import app_views BP from api.v1.views
from models import storage  # Imports the storage instance from models package
import os


# Set up the Flask app
app = Flask(__name__)

# Register the app_views blueprint to the Flask instance app
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close storage session."""
    storage.close()


# Custom 404 error handler
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
