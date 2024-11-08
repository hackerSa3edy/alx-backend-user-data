#!/usr/bin/env python3
"""Module for handling password encryption using bcrypt.
Provides functions to hash passwords and validate hashed passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with salt.

    Args:
        password (str): The password string to hash

    Returns:
        bytes: The salted password hash
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate whether a password matches its hashed version.

    Args:
        hashed_password (bytes): The hashed password to check against
        password (str): The password to validate

    Returns:
        bool: True if password matches the hash, False otherwise
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
