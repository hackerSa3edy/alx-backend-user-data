#!/usr/bin/env python3
""" User module
Contains the User class for handling user authentication and data management.
"""
import hashlib
from models.base import Base
from typing import Optional


class User(Base):
    """
    User class with optimized methods for authentication and user management.

    This class extends the Base class and provides functionality for:
    - User data storage and retrieval
    - Password hashing and validation
    - User display name formatting

    Attributes:
        email (str): User's email address
        _password (str): Hashed password
        first_name (str): User's first name
        last_name (str): User's last name
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance with provided attributes.

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments containing user attributes
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> Optional[str]:
        """ Retrieve the hashed password.

        Returns:
            Optional[str]: The hashed password or None if not set
        """
        return self._password

    @staticmethod
    def _hash_password(pwd: str) -> str:
        """ Hash a password string using SHA256.

        Args:
            pwd (str): Plain text password to hash

        Returns:
            str: Lowercase hexadecimal string of hashed password
        """
        return hashlib.sha256(pwd.encode()).hexdigest().lower()

    @password.setter
    def password(self, pwd: str) -> None:
        """ Set a new password by hashing it with SHA256.

        Args:
            pwd (str): Plain text password to be hashed and stored
        """
        self._password = self._hash_password(pwd) if isinstance(
            pwd,
            str
            ) else None

    def is_valid_password(self, pwd: str) -> bool:
        """ Validate if provided password matches stored hash.

        Args:
            pwd (str): Plain text password to validate

        Returns:
            bool: True if password matches, False otherwise
        """
        if not isinstance(pwd, str) or self.password is None:
            return False
        return self._hash_password(pwd) == self.password

    def display_name(self) -> str:
        """ Generate a display name based on available user information.

        Returns:
            str: Formatted display name using the following priority:
                1. First name + Last name
                2. First name or Last name (if only one is available)
                3. Email
                4. Empty string if no information is available
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return (self.first_name or self.last_name or self.email or "")
