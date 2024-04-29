#!/usr/bin/python3
"""
Createnew Flask app; and reg blueprint app_views to the Flask instance app.
"""
# Import necessary modules
from os import getenv
from flask import Flask, jsonify
from models import storage  # Imports the storage instance from models package
from api.v1.views import app_views  # Import app_views BP from api.v1.views


# Create a Flask app instance
app = Flask(__name__)

# Register the app_views blueprint to the Flask instance app
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown function
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 error
    :return: returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return(resp)

# Main entry point of the application
if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
