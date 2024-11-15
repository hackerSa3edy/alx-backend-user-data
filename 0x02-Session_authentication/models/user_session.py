#!/usr/bin/env python3
""" User Sessions Model
Defines the UserSession class for managing user sessions.
"""
from models.base import Base


class UserSession(Base):
    """ User Session class for storing user session information.

    Attributes:
        user_id (str): The ID of the user.
        session_id (str): The session ID.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance.

        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
