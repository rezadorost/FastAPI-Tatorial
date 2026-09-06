# FastAPI Tutorial

A simple FastAPI learning project built step by step while learning Python backend development.

## Features

- FastAPI application
- Uvicorn server
- GET, POST, PUT, and DELETE endpoints
- Query parameters
- Path parameters
- JSON request bodies
- Pydantic models
- CRUD operations using a SQLite database
- HTTP status codes
- Error handling with `HTTPException`
- Response models
- Pydantic field validation
- Custom validation with `field_validator`
- Default field values
- Basic project structure using `APIRouter`
- Dependency Injection
- SQLAlchemy ORM
- Database sessions
- Database CRUD operations

## Project Structure

```text
FastAPI-Tatorial/
│
├── core/
│   ├── database.py    # Database configuration and session management
│   ├── main.py        # FastAPI application setup and router registration
│   ├── models.py      # Pydantic schemas and SQLAlchemy ORM models
│   └── routes.py      # API endpoints and database operations
│
├── docs/
├── .gitignore
├── README.md
└── requirements.txt
```

## Application Structure

### `main.py`

Creates and configures the FastAPI application.

It connects the router to the application and initializes the database tables.

```python
app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)
```

### `database.py`

Contains the database configuration.

It is responsible for:

- Creating the database URL
- Creating the SQLAlchemy engine
- Creating database sessions
- Providing a database session through Dependency Injection

The general flow is:

```text
DATABASE_URL
      ↓
Engine
      ↓
SessionLocal
      ↓
get_db()
      ↓
Endpoint / Dependency
```

### `models.py`

Contains both Pydantic models and SQLAlchemy ORM models.

Pydantic models are used for request and response validation.

SQLAlchemy models are used to map Python classes to database tables.

The project currently includes:

- `Name`
- `NameResponse`
- `Names`

The `Names` SQLAlchemy model represents the `names` table in the SQLite database:

```text
Names
├── id
├── name
└── age
```

### `routes.py`

Contains the API routes and endpoints.

The current project supports:

```text
GET     /
GET     /names/{id}
POST    /names
PUT     /names/{id}
DELETE  /names/{id}
```

The CRUD endpoints currently use SQLAlchemy and SQLite for database operations.

## Validation

The `Name` model currently validates the following:

- `id` must be greater than `0`
- `name` must contain at least `2` characters
- `name` must contain at most `20` characters
- Leading and trailing spaces are removed
- A name containing only spaces is rejected
- `age` has a default value of `18`

## Response Models

The project uses a response model for retrieving data:

```python
class NameResponse(BaseModel):
    id: int
    name: str
    age: int
```

This controls and validates the data returned by the API.

## Error Handling

If a requested ID does not exist, the API returns:

```text
404 Not Found
```

using:

```python
raise HTTPException(
    status_code=404,
    detail="Not Found"
)
```

Invalid request data is automatically handled by FastAPI and Pydantic with:

```text
422 Unprocessable Entity
```

## Database Integration

The project uses the following flow:

```text
FastAPI
   ↓
Dependency Injection
   ↓
SQLAlchemy Session
   ↓
SQLAlchemy ORM
   ↓
SQLite Database
```

### Session Management

A database session is provided using the `get_db` dependency.

The general flow is:

```text
Request
   ↓
SessionLocal()
   ↓
yield db
   ↓
Endpoint / Dependency uses the Session
   ↓
Request finishes
   ↓
db.close()
```

Closing the Session does not remove committed data from the database.

### CRUD Operations

The current CRUD operations work with the database:

```text
POST
→ Create a SQLAlchemy object
→ db.add()
→ db.commit()

GET
→ db.get()

DELETE
→ db.delete()
→ db.commit()

PUT
→ Update the SQLAlchemy object
→ db.commit()
```

## Dependency Injection

Dependencies are used to provide reusable functionality to endpoints.

The project currently uses dependencies for:

- Providing a database Session with `get_db`
- Checking whether a requested ID exists with `check_name_id`

A dependency can also depend on another dependency:

```text
Endpoint
   ↓
Depends(check_name_id)
   ↓
check_name_id
   ↓
Depends(get_db)
   ↓
Database Session
```

The result of one dependency can also be passed to an endpoint:

```text
check_name_id
   ↓
Find record in database
   ↓
Return Names object
   ↓
Endpoint receives the Names object
```

## Running the Project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Make sure you are in the project root directory:

```text
FastAPI-Tatorial/
```

Run the application:

```bash
uvicorn core.main:app --reload
```

The API will run locally.

You can access the interactive Swagger documentation at:

`http://127.0.0.1:8000/docs`

## Current Status

This project is currently being used as a learning project for FastAPI.

Completed topics:

- [x] FastAPI setup
- [x] Uvicorn
- [x] Routes and endpoints
- [x] HTTP methods
- [x] Query parameters
- [x] Path parameters
- [x] Request body and JSON
- [x] Pydantic `BaseModel`
- [x] Basic CRUD
- [x] HTTP status codes
- [x] `HTTPException`
- [x] Basic error handling
- [x] Response models
- [x] Pydantic validation
- [x] Optional and default fields
- [x] Custom validation
- [x] Basic project structure
- [x] Dependency Injection
- [x] SQLite database
- [x] SQLAlchemy Engine
- [x] SQLAlchemy Session
- [x] SQLAlchemy ORM models
- [x] Database CRUD operations
- [x] Mini project

Next topics include:

- Database Relationships
- Authentication
- JWT
- Testing
- Docker
- Deployment

# IMPORTANT

## Learning Approach

This project is developed incrementally as part of a deep learning journey into FastAPI and Python backend development.

The goal is not simply to build a working application. Each feature and technology is introduced step by step, implemented, tested, and then refactored as the project grows.

The project intentionally evolves over time so that each stage provides an opportunity to understand the underlying concepts, architecture, and interaction between different components.

Therefore, the current state of the code should be viewed as a snapshot of an ongoing learning process rather than the final architecture of the application.

## Project Evolution

The learning process follows a gradual progression:

```text
FastAPI Fundamentals
        ↓
Routing & HTTP
        ↓
Pydantic & Validation
        ↓
Error Handling
        ↓
Dependency Injection
        ↓
SQLAlchemy / ORM
        ↓
Database Integration
        ↓
Authentication
        ↓
Testing
        ↓
Docker & Deployment
```

Each stage builds upon the concepts learned in the previous stages.