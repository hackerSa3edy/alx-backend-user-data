#!/usr/bin/env python3
"""
Route module for the API with improved organization and error handling
"""
from os import getenv
from typing import Tuple, Any

from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

# App Configuration
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Authentication Configuration
AUTH_TYPE_MAP = {
    "basic_auth": BasicAuth,
    "auth": Auth
}
auth_type = getenv("AUTH_TYPE")
auth = AUTH_TYPE_MAP.get(auth_type)() if auth_type in AUTH_TYPE_MAP else None

# Error Handler Types
ErrorResponse = Tuple[dict, int]


def error_response(message: str, status_code: int) -> ErrorResponse:
    """Generic error response handler"""
    return jsonify({"error": message}), status_code


@app.errorhandler(404)
def not_found(error) -> ErrorResponse:
    """Not found handler"""
    return error_response("Not found", 404)


@app.errorhandler(401)
def unauthorized(error) -> ErrorResponse:
    """Unauthorized handler"""
    return error_response("Unauthorized", 401)


@app.errorhandler(403)
def forbidden(error) -> ErrorResponse:
    """Forbidden handler"""
    return error_response("Forbidden", 403)


@app.before_request
def handle_auth() -> Any:
    """Authentication middleware"""
    if not auth:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if not auth.authorization_header(request):
        abort(401)

    if not auth.current_user(request):
        abort(403)


if __name__ == "__main__":
    app.run(
        host=getenv("API_HOST", "0.0.0.0"),
        port=getenv("API_PORT", "5000")
    )
