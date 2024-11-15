#!/usr/bin/env python3
""" User module
Defines the User class for managing user data.
"""
import hashlib
from models.base import Base


class User(Base):
    """ User class
    Represents a user with email, password, first name, and last name.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """ Getter of the password
        Returns:
            str: The hashed password.
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Setter of a new password: encrypt in SHA256
        Args:
            pwd (str): The new password to be hashed.
        """
        if isinstance(pwd, str):
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()
        else:
            self._password = None

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate a password
        Args:
            pwd (str): The password to validate.
        Returns:
            bool: True if the password is valid, False otherwise.
        """
        if not isinstance(pwd, str) or self.password is None:
            return False
        hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest().lower()
        return hashed_pwd == self.password

    def display_name(self) -> str:
        """ Display User name based on email, first name, and last name
        Returns:
            str: The user's display name.
        """
        if self.email and not self.first_name and not self.last_name:
            return self.email
        if self.first_name and not self.last_name:
            return self.first_name
        if self.last_name and not self.first_name:
            return self.last_name
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return ""
