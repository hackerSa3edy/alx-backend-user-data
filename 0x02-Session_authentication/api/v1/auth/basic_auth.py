#!/usr/bin/env python3
"""Implement basic auth for end points API"""
from typing import TypeVar

from api.v1.auth.auth import Auth
import base64

from models.user import User


class BasicAuth(Auth):
    """ Basic auth class"""

    def extract_base64_authorization_header(
            self,
            authorization_header: str
    ) -> str:
        """Returns base64 of Authorization header"""
        if not authorization_header or type(authorization_header) != str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of a Base64 string"""
        if (not base64_authorization_header
                or type(base64_authorization_header) != str):
            return None

        try:
            return (base64.b64decode(base64_authorization_header)
                    .decode('utf-8'))
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value"""
        if (not decoded_base64_authorization_header
                or type(decoded_base64_authorization_header) != str
                or decoded_base64_authorization_header.find(":") == -1):
            return None, None

        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if not user_email or type(user_email) != str:
            return None

        if not user_pwd or type(user_pwd) != str:
            return None

        user = User()
        user_objs = user.search({"email": user_email})
        if not user_objs:
            return None

        if not user_objs[0].is_valid_password(user_pwd):
            return None

        return user_objs[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        base64_credentials = self.extract_base64_authorization_header(
            auth_header)
        decoded_credentials = self.decode_base64_authorization_header(
            base64_credentials)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_credentials)
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
