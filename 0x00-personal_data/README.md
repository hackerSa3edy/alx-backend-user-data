# 0x00. Personal Data

## Overview

This project focuses on implementing personal data security practices in Python. It covers regex operations for filtering sensitive information, secure logging practices, password hashing, and database security fundamentals.

## Resources

### Read or watch

* [What Is PII, non-PII, and Personal Data?](https://piwik.pro/blog/what-is-pii-personal-data/)
* [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
* [bcrypt Package Documentation](https://pypi.org/project/bcrypt/)
* [Logging to Files, Setting Levels, and Formatting](https://realpython.com/python-logging/)

## Tasks

| Task | File | Description |
|------|------|-------------|
| 0. Regex-ing | [filtered_logger.py](./filtered_logger.py) | Implement a function to obfuscate sensitive fields in log messages using regex |
| 1. Log formatter | [filtered_logger.py](./filtered_logger.py) | Create a custom RedactingFormatter class to automatically filter PII data in logs |
| 2. Create logger | [filtered_logger.py](./filtered_logger.py) | Implement a get_logger function that returns a configured Logger object |
| 3. Connect to secure database | [filtered_logger.py](./filtered_logger.py) | Create a get_db function to securely connect to a MySQL database |
| 4. Read and filter data | [filtered_logger.py](./filtered_logger.py) | Implement main function to retrieve and display filtered user data |
| 5. Encrypting passwords | [encrypt_password.py](./encrypt_password.py) | Create a function to encrypt passwords using bcrypt |
| 6. Check valid password | [encrypt_password.py](./encrypt_password.py) | Implement password validation against hashed password |

## Implementation Details

### filtered_logger.py

* Uses regex pattern matching for PII field filtering
* Implements secure logging with custom formatter
* Provides database connection management using context managers
* Handles environment variables for secure configuration
* PII fields protected: name, email, phone, ssn, password
