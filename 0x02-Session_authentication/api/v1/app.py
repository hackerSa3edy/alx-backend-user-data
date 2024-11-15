#!/usr/bin/env python3
"""
API Route Module

This module sets up the Flask application, registers blueprints,
and configures CORS.
It also handles different types of authentication based on
environment variables.
Error handlers for common HTTP errors are defined, and a before_request
function is used to manage authentication for incoming requests.
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv("AUTH_TYPE")

auth_classes = {
    "basic_auth": BasicAuth,
    "session_auth": SessionAuth,
    "auth": Auth,
    "session_exp_auth": SessionExpAuth,
    "session_db_auth": SessionDBAuth
}

if auth_type in auth_classes:
    auth = auth_classes[auth_type]()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def handle_auth() -> None:
    """Handle authorization before sending requests"""
    if not auth:
        return

    excluded_list = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]
    if not auth.require_auth(request.path, excluded_list):
        return

    if not auth.authorization_header(request) and \
       not auth.session_cookie(request):
        abort(401)

    request.current_user = auth.current_user(request)
    if not request.current_user:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
