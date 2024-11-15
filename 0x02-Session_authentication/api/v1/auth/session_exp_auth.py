#!/usr/bin/env python3
"""Session Expiration Auth"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class"""

    def __init__(self):
        """ Init the session duration"""
        self.session_duration = int(getenv("SESSION_DURATION", "0"))

    def create_session(self, user_id=None):
        """ Create session with expr time"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get the allowed user id only"""
        if not session_id:
            return None

        if not self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if not created_at:
            return None

        allowed_time = created_at + timedelta(seconds=self.session_duration)
        if allowed_time < datetime.now():
            return None

        return session_dict.get("user_id")
