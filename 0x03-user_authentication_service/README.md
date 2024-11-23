# Project: 0x03. User authentication service

A secure user authentication service using Python, Flask and SQLAlchemy. This project implements a user authentication system with features like user registration, login/logout, password reset, and session management.

## Table of Contents

- [Overview](#overview)
- [Resources](#resources)
- [API Endpoints](#api-endpoints)
- [Tasks](#tasks)
- [Setup](#setup)

## Overview

This authentication system provides:

- User registration and account management
- Secure password hashing
- Session-based authentication
- Password reset functionality
- RESTful API endpoints

## Resources

- [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/)
- [Requests module](https://docs.python-requests.org/en/latest/)
- [HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## API Endpoints

| Method | Endpoint                    | Description                                   |
|--------|----------------------------|-----------------------------------------------|
| POST   | /users                     | Register new user                             |
| POST   | /sessions                  | Login user and create session                 |
| DELETE | /sessions                  | Logout user and destroy session               |
| GET    | /profile                   | Get user profile information                  |
| POST   | /reset_password            | Generate password reset token                 |
| PUT    | /reset_password            | Update password using reset token             |

## Tasks

| Task | File | Description |
|------|------|-------------|
| 0. User model | [user.py](./user.py) | Create SQLAlchemy model for storing user data |
| 1. create user | [db.py](./db.py) | Implement user creation in database |
| 2. Find user | [db.py](./db.py) | Add methods to find user by email/id |
| 3. update user | [db.py](./db.py) | Implement user information updates |
| 4. Hash password | [auth.py](./auth.py) | Add secure password hashing |
| 5. Register user | [auth.py](./auth.py) | Implement user registration logic |
| 6. Basic Flask app | [app.py](./app.py) | Setup basic Flask application |
| 7. Register user | [app.py](./app.py) | Add registration endpoint |
| 8. Credentials validation | [auth.py](./auth.py) | Validate user credentials |
| 9. Generate UUIDs | [auth.py](./auth.py) | Generate unique session IDs |
| 10. Get session ID | [auth.py](./auth.py) | Create user sessions |
| 11. Log in | [app.py](./app.py) | Implement login endpoint |
| 12. Find user by session ID | [auth.py](./auth.py) | Retrieve user from session |
| 13. Destroy session | [auth.py](./auth.py) | Implement session cleanup |
| 14. Log out | [app.py](./app.py) | Add logout endpoint |
| 15. User profile | [app.py](./app.py) | Create profile endpoint |
| 16. Generate reset password token | [auth.py](./auth.py) | Implement password reset tokens |
| 17. Get reset password token | [app.py](./app.py) | Add reset token endpoint |
| 18. Update password | [auth.py](./auth.py) | Handle password updates |
| 19. Update password end-point | [app.py](./app.py) | Create password update endpoint |
| 20. End-to-end integration test | [main.py](./main.py) | Complete system testing |
