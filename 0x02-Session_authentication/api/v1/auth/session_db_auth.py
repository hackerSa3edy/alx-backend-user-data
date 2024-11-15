#!/usr/bin/env python3
"""Implement session auth for end points API"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """ Creates and stores new instance of UserSession
            and returns the Session ID"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user = UserSession(
            **{"session_id": session_id, "user_id": user_id}
        )
        user.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the User ID by requesting UserSession
            in the database based on session_id"""
        if not session_id:
            return None

        UserSession.load_from_file()
        user_sessions = UserSession.search({"session_id": session_id})

        if not user_sessions:
            return None

        user_session = user_sessions[0]
        expired_time = (user_session.created_at +
                        timedelta(seconds=self.session_duration))

        if expired_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID
            from the request cookie"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        user_session = UserSession.search({
            'session_id': session_id
        })

        if not user_session:
            return False

        user_session = user_session[0]

        try:
            user_session.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
