# FastAPI Tutorial API

A RESTful API built with **FastAPI**, **SQLAlchemy**, and **SQLite** as a hands-on Python backend development project.

This project covers database integration, CRUD operations, user authentication, JWT-based access control, and role-based permissions.

## Features

- FastAPI application and RESTful API endpoints
- Pydantic request and response validation
- SQLAlchemy ORM and SQLite database
- Database sessions and dependency injection
- One-to-many relationships between users and phone numbers
- User registration and login
- Password hashing
- JWT authentication
- Protected endpoints
- Role-Based Access Control (RBAC)
- Permission-based authorization
- Admin user management
- User promotion and demotion
- Protection against demoting the last administrator
- Interactive API documentation with Swagger UI and ReDoc

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation |
| SQLAlchemy | ORM and database operations |
| SQLite | Database |
| PyJWT | JWT creation and validation |
| pwdlib | Password hashing |

## Project Structure

```text
FastAPI-Tatorial/
│
├── core/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── make_admin.py
│   ├── models.py
│   └── routes.py
│
├── docs/
├── .venv/
├── names.db
├── requirements.txt
└── README.md
```

### Main Components

**`core/main.py`**

Creates and configures the FastAPI application, registers the router, and initializes database tables.

**`core/database.py`**

Contains the SQLite database configuration, SQLAlchemy engine, declarative base, session factory, and database dependency.

**`core/models.py`**

Contains SQLAlchemy database models and Pydantic schemas.

**`core/routes.py`**

Contains API endpoints, database operations, and authorization dependencies.

**`core/auth.py`**

Contains password hashing, password verification, JWT handling, current-user authentication, role permissions, and permission-checking dependencies.

**`core/make_admin.py`**

A utility script for assigning the administrator role to a user.

## Database Design

The application currently uses two main database models:

### Users

| Field | Description |
|---|---|
| `id` | User ID |
| `username` | Unique username |
| `email` | Unique email address |
| `hashed_password` | Hashed password |
| `role` | User role, defaulting to `user` |

### PhoneNumbers

| Field | Description |
|---|---|
| `id` | Phone number ID |
| `number` | Phone number |
| `user_id` | Foreign key referencing `Users.id` |

### Relationship

The application implements a one-to-many relationship:

```text
One User
   |
   ├── Phone Number
   ├── Phone Number
   └── Phone Number
```

Each user can have multiple phone numbers, while each phone number belongs to one user.

## Authentication

Authentication verifies the identity of a user.

The application uses:

- Password hashing with `pwdlib`
- Password verification during login
- JWT access tokens
- OAuth2 Bearer token authentication
- A protected current-user dependency

### Registration

```http
POST /users/register
```

Creates a new user account.

Example request:

```json
{
    "username": "example_user",
    "email": "example@example.com",
    "password": "your-password"
}
```

Duplicate usernames and email addresses are rejected.

### Login

```http
POST /users/login
```

Authenticates a user and returns a JWT access token.

The login endpoint uses OAuth2 password form data.

Example response:

```json
{
    "access_token": "your-access-token",
    "token_type": "bearer"
}
```

### Current User

```http
GET /users/me
```

Returns information about the authenticated user.

Protected endpoints require a valid Bearer token.

## Authorization

Authorization determines what an authenticated user is allowed to do.

The project implements **Role-Based Access Control (RBAC)**.

### Roles

The current roles are:

- `user`
- `admin`

### Permissions

Permissions define which operations a role can perform.

Examples include:

```text
users:read
users:update
users:delete
users:promote
users:demote
admins:read
phone_numbers:read_own
phone_numbers:create
phone_numbers:update_own
phone_numbers:delete_own
```

Permissions are mapped to roles in `ROLE_PERMISSIONS`.

The `require_permission()` dependency checks whether the authenticated user's role has the required permission.

The user's role is retrieved from the database during authentication, rather than being stored in the JWT payload.

### Administrator Operations

Administrators can:

- View all users
- View an individual user
- Update user information
- Delete users
- View administrators
- Promote users to administrators
- Demote administrators to regular users

The application also prevents demoting the last remaining administrator.

## API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |

### Phone Numbers

| Method | Endpoint | Description |
|---|---|---|
| POST | `/phone-numbers` | Add a phone number |
| GET | `/phone-numbers` | Get the current user's phone numbers |
| PUT | `/phone-numbers/{phone_id}` | Update an owned phone number |
| DELETE | `/phone-numbers/{phone_id}` | Delete an owned phone number |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a user |
| POST | `/users/login` | Authenticate a user |
| GET | `/users/me` | Get the current user's profile |

### Admin

| Method | Endpoint | Permission |
|---|---|---|
| GET | `/admin` | `users:read` |
| GET | `/admin/users` | `users:read` |
| GET | `/admin/users/{user_id}` | `users:read` |
| PUT | `/admin/users/{user_id}` | `users:update` |
| DELETE | `/admin/users/{user_id}` | `users:delete` |
| GET | `/admin/users/admins` | `admins:read` |
| PATCH | `/admin/users/{user_id}/promote` | `users:promote` |
| PATCH | `/admin/users/{user_id}/demote` | `users:demote` |

## Error Handling

The API uses appropriate HTTP status codes.

| Status Code | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 204 | Resource deleted |
| 400 | Bad request |
| 401 | Authentication required or invalid credentials |
| 403 | Insufficient permissions |
| 404 | Resource not found |
| 409 | Resource conflict, such as duplicate username or email |
| 422 | Request validation error |

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/rezadorost/FastAPI-Tatorial.git
cd FastAPI-Tatorial
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

On Linux and macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
uvicorn core.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive API documentation.

**Swagger UI**

```text
http://127.0.0.1:8000/docs
```

**ReDoc**

```text
http://127.0.0.1:8000/redoc
```

These interfaces allow developers to explore API endpoints, inspect schemas, and test requests.

## Current Project Status

This repository is an evolving backend learning project.

Completed areas:

- [x] FastAPI fundamentals
- [x] Routing and HTTP methods
- [x] Pydantic validation
- [x] Response models
- [x] Error handling
- [x] Dependency injection
- [x] SQLite integration
- [x] SQLAlchemy ORM
- [x] Database relationships
- [x] CRUD operations
- [x] Password hashing
- [x] JWT authentication
- [x] Protected routes
- [x] Role-Based Access Control
- [x] Permission-based authorization
- [x] Administrator management
- [x] API documentation

Further development will continue as the backend learning roadmap progresses.

## Learning Approach

This project is developed incrementally.

Each feature is implemented and tested while learning the underlying backend concepts. The goal is to understand how the components work together and gradually build the skills required for professional Python backend development.