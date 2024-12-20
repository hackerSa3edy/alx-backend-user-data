#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


def get_user_by_id(user_id: str):
    """Helper function to get user by ID or abort if not found"""
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - JSON list of all User objects
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - user_id: ID of the User
    Return:
      - JSON representation of the User object
      - 404 if the User ID doesn't exist
    """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = get_user_by_id(user_id)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - user_id: ID of the User
    Return:
      - empty JSON if the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    user = get_user_by_id(user_id)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email: User's email
      - password: User's password
      - last_name (optional): User's last name
      - first_name (optional): User's first name
    Return:
      - JSON representation of the created User object
      - 400 if can't create the new User
    """
    try:
        rj = request.get_json()
        if not rj:
            raise ValueError("Wrong format")
        if not rj.get("email"):
            raise ValueError("email missing")
        if not rj.get("password"):
            raise ValueError("password missing")

        user = User(
            email=rj.get("email"),
            password=rj.get("password"),
            first_name=rj.get("first_name"),
            last_name=rj.get("last_name")
        )
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - user_id: ID of the User
    JSON body:
      - last_name (optional): User's last name
      - first_name (optional): User's first name
    Return:
      - JSON representation of the updated User object
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    user = get_user_by_id(user_id)
    try:
        rj = request.get_json()
        if not rj:
            raise ValueError("Wrong format")

        if 'first_name' in rj:
            user.first_name = rj.get('first_name')
        if 'last_name' in rj:
            user.last_name = rj.get('last_name')

        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
