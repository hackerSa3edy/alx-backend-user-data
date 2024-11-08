#!/usr/bin/env python3
"""Module for handling personal data and logging with privacy in mind."""

from typing import List, Tuple
import logging
import os
import re
from contextlib import contextmanager

import mysql.connector
from mysql.connector.connection import MySQLConnection

# Constants
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")
DEFAULT_DB_HOST: str = "localhost"
DEFAULT_DB_USER: str = "root"
DEFAULT_DB_PASSWORD: str = ""
DEFAULT_DB_PORT: int = 3306


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message with specified fields obfuscated.

    Args:
        fields: List of strings representing fields to redact
        redaction: String to replace sensitive info with
        message: String representing the log line
        separator: String separator character
    """
    pattern = rf'({"|".join(fields)})=([^{separator}]+)'
    return re.sub(pattern, rf'\1={redaction}', message)


def get_logger() -> logging.Logger:
    """Returns a configured logger for user data."""
    logger = logging.getLogger("user_data")
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


@contextmanager
def get_db() -> MySQLConnection:
    """
    Context manager for database connection.
    Returns a configured MySQL database connection.
    """
    db = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", DEFAULT_DB_HOST),
        port=DEFAULT_DB_PORT,
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", DEFAULT_DB_USER),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", DEFAULT_DB_PASSWORD),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    try:
        yield db
    finally:
        db.close()


def main() -> None:
    """Main function to demonstrate logging of user data."""
    logger = get_logger()

    try:
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            column_names = cursor.column_names

            for user in users:
                user_data = dict(zip(column_names, user))
                formatted_user = "; ".join(
                    f"{key}={value}" for key, value in user_data.items()
                )
                logger.info(formatted_user)

            cursor.close()
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
    except Exception as err:
        logger.error(f"Unexpected error: {err}")


class RedactingFormatter(logging.Formatter):
    """Formatter class to redact sensitive information in logs."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with sensitive information redacted."""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            str(record.msg),
            self.SEPARATOR
            )
        return super().format(record)


if __name__ == '__main__':
    main()
