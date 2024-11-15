#!/usr/bin/env python3
"""Implement session auth for end points API"""
import uuid

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session auth class"""

    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session id for a user"""
        if not user_id or type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID"""
        if not session_id or type(session_id) != str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value"""
        if not request:
            return

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ Deletes the user session"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]

        return True
