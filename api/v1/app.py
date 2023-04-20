#!/usr/bin/python3
"""
contains the flask web app
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
host = os.getenv("HBNB_API_HOST", "0.0.0.0")
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': host}})
app.url_map.strict_slashes = False

@app.teardown_appcontext
def teardown_app_context(exception):
    """Close the storage session."""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''Handles the 404 HTTP error code.'''
    return jsonify(error='Not found'), 404

@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code.'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
