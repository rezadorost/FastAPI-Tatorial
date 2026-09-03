# FastAPI Tutorial

A simple FastAPI learning project built step by step while learning Python backend development.

## Features

* FastAPI application
* Uvicorn server
* GET, POST, PUT, and DELETE endpoints
* Query parameters
* Path parameters
* JSON request bodies
* Pydantic models
* CRUD operations using temporary in-memory storage
* HTTP status codes
* Error handling with `HTTPException`
* Response models
* Pydantic field validation
* Custom validation with `field_validator`
* Default field values
* Basic project structure using `APIRouter`

## Project Structure

```text
FastAPI-Tatorial/
│
├── core/
│   ├── main.py        # FastAPI application and router registration
│   ├── models.py      # Pydantic models and validation
│   └── routes.py      # API endpoints and temporary storage
│
├── docs/
├── .gitignore
├── README.md
├── requirements.txt
└── .venv/
```

## Application Structure

### `main.py`

Creates the FastAPI application and connects the router to the application.

```python
app = FastAPI()

app.include_router(router)
```

### `models.py`

Contains Pydantic models used for request validation and response validation.

The project currently includes:

* `Name`
* `NameResponse`
* Field validation using `Field()`
* Custom name validation using `@field_validator`

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

## Validation

The `Name` model currently validates the following:

* `id` must be greater than `0`
* `name` must contain at least `2` characters
* `name` must contain at most `20` characters
* Leading and trailing spaces are removed
* A name containing only spaces is rejected
* `age` has a default value of `18`

## Response Models

The project uses a response model for retrieving a name:

```python
class NameResponse(BaseModel):
    id: int
    name: str
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

## Running the Project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Move to the `core` directory:

```bash
cd core
```

Run the application:

```bash
python main.py
```

The API will run locally, and you can access the interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

## Current Status

This project is currently being used as a learning project for FastAPI.

Completed topics:

* [x] FastAPI setup
* [x] Uvicorn
* [x] Routes and endpoints
* [x] HTTP methods
* [x] Query parameters
* [x] Path parameters
* [x] Request body and JSON
* [x] Pydantic `BaseModel`
* [x] Basic CRUD
* [x] HTTP status codes
* [x] `HTTPException`
* [x] Basic error handling
* [x] Response models
* [x] Pydantic validation
* [x] Optional and default fields
* [x] Custom validation
* [x] Basic project structure

Next topics include:

* Dependencies
* Mini project
* Database
* SQLAlchemy / ORM
* Authentication
* JWT
* Testing
* Docker
* Deployment
