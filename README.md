# FastAPI Tutorial

A practical Python backend development project built with **FastAPI**, **SQLAlchemy**, **Pydantic**, and **JWT**.

This project demonstrates the development of a RESTful API with user management, phone number management, authentication, and role-based authorization.

## Features

### API Development
- RESTful API development with FastAPI.
- CRUD operations.
- Path and query parameters.
- Request validation using Pydantic.
- Response models.
- HTTP exception handling.
- Dependency Injection.

### Database
- SQLite database.
- SQLAlchemy ORM.
- Declarative database models.
- Foreign key relationships.
- One-to-many relationships.
- Database session management.
- Cascade operations.

### Authentication
- User registration and login.
- Password hashing and verification with `pwdlib`.
- JWT access token generation and validation.
- Token expiration.
- OAuth2 Bearer authentication.
- Authenticated user retrieval.

### Authorization
- Role-Based Access Control (RBAC).
- Permission-based authorization.
- User and administrator roles.
- Protected API endpoints.
- Resource ownership checks.
- Administrative user management.
- User promotion and demotion.
- Protection against deleting the current administrator.
- Protection against demoting the last administrator.

### API Documentation
- Automatic OpenAPI documentation.
- Swagger UI.
- ReDoc.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| SQLAlchemy | ORM |
| SQLite | Database |
| Pydantic | Data validation |
| PyJWT | JWT handling |
| pwdlib | Password hashing |

## Project Structure

```text
FastAPI-Tatorial/
│
├── core/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── make_admin.py
│   ├── models.py
│   └── routes.py
│
├── requirements.txt
└── README.md
```

## Application Architecture

### Database Models

The application uses two main database models:

**Users**

Stores user account information:
- `id`
- `username`
- `email`
- `hashed_password`
- `role`

Usernames and email addresses are unique. Newly registered users receive the `user` role by default.

**PhoneNumbers**

Stores phone numbers associated with user accounts.

The relationship between `Users` and `PhoneNumbers` is one-to-many: a user can have multiple phone numbers, while each phone number belongs to one user.

### Authentication Flow

1. A user registers with a username, email, and password.
2. The password is hashed before it is stored.
3. The user submits login credentials.
4. The application verifies the password.
5. A JWT access token is generated.
6. The client sends the token with protected requests.
7. The application validates the token and retrieves the user from the database.

### Authorization Flow

Authentication identifies the user. Authorization determines which operations that user can perform.

The application uses roles and permissions:

- `user`: access to permitted operations on their own phone numbers.
- `admin`: access to administrative user-management operations.

Permission checks are implemented through FastAPI dependencies. Ownership checks ensure that regular users cannot modify another user's phone numbers.

## API Endpoints

The following endpoints are implemented in the application.

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |

### Phone Numbers

| Method | Endpoint | Description |
|---|---|---|
| POST | `/phone-numbers` | Create a phone number |
| GET | `/phone-numbers` | Retrieve the current user's phone numbers |
| PUT | `/phone-numbers/{phone_id}` | Update an owned phone number |
| DELETE | `/phone-numbers/{phone_id}` | Delete an owned phone number |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a new user |
| POST | `/users/login` | Authenticate and receive an access token |
| GET | `/users/me` | Retrieve the authenticated user's profile |

### Administration

| Method | Endpoint | Description |
|---|---|---|
| GET | `/admin` | Access the admin dashboard |
| GET | `/admin/users` | Retrieve all users |
| GET | `/admin/users/{user_id}` | Retrieve a specific user |
| PUT | `/admin/users/{user_id}` | Update user information |
| DELETE | `/admin/users/{user_id}` | Delete a user |
| GET | `/admin/users/admins` | Retrieve administrator accounts |
| PATCH | `/admin/users/{user_id}/promote` | Promote a user to administrator |
| PATCH | `/admin/users/{user_id}/demote` | Demote an administrator to regular user |

Administrative endpoints require the appropriate permissions.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rezadorost/FastAPI-Tatorial.git
cd FastAPI-Tatorial
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the application

Run this command from the project root:

```bash
python -m uvicorn core.main:app --reload
```

The application will be available at:

`http://127.0.0.1:8000`

## API Documentation

After starting the application, access the automatically generated documentation:

| Interface | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

Swagger UI can be used to explore endpoints, submit requests, and test authenticated operations.

## HTTP Status Codes

| Status Code | Description |
|---|---|
| `200` | OK |
| `204` | No Content |
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `409` | Conflict |
| `422` | Unprocessable Entity |

## Learning Objectives

This repository is part of a practical backend development learning process.

The concepts implemented so far include:

- Python backend development.
- RESTful API design.
- FastAPI application structure.
- Pydantic schemas and validation.
- SQLAlchemy ORM and relationships.
- Database sessions.
- Dependency Injection.
- Password hashing.
- JWT authentication.
- OAuth2 Bearer authentication.
- Role-Based Access Control.
- Permission-based authorization.
- Resource ownership checks.
- API documentation.
- Git and GitHub workflow.

## Security Notes

This repository is currently an educational project intended for development and learning.

Before production deployment, security configuration must be reviewed. In particular, the JWT secret key should be supplied through secure environment configuration rather than hardcoded in the source code.

## Author

**Reza Dorost**

GitHub: [@rezadorost](https://github.com/rezadorost)

Repository: [FastAPI-Tatorial](https://github.com/rezadorost/FastAPI-Tatorial)

---

## Acknowledgment

**This README.md file was written by ChatGPT (OpenAI).**
