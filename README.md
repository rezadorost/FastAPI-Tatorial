# FastAPI Tutorial 🚀

A hands-on FastAPI learning project built step by step while learning the fundamentals of Python backend development.

This repository contains a simple **Names API** that is being developed progressively to practice FastAPI concepts and REST API fundamentals.

## 📂 Project Structure

```text
FastAPI-Tutorial/
│
├── core/
│   └── main.py
│
├── docs/
│
├── .gitignore
├── README.md
├── requirements.txt
│
└── .venv/              # ignored by Git
```

## 🛠️ Technologies

* Python 3
* FastAPI
* Uvicorn
* Pydantic

## 📌 Current Features

* FastAPI application setup
* Uvicorn server
* GET requests
* POST requests
* PUT requests
* DELETE requests
* Path parameters
* Query parameters
* JSON request bodies
* Pydantic models
* Basic CRUD operations
* Swagger UI for API testing

## 📖 API Endpoints

### GET `/`

Returns a simple welcome message.

```http
GET /
```

### GET `/names`

Uses query parameters.

```http
GET /names?id=3&name=Amir
```

### GET `/names/{id}`

Returns a name using its ID.

```http
GET /names/3
```

### POST `/names`

Creates a new name using a JSON request body.

Example:

```json
{
    "id": 4,
    "name": "Darius"
}
```

### PUT `/names/{id}`

Updates an existing name.

Example:

```http
PUT /names/2?name=Darius
```

### DELETE `/names/{id}`

Deletes a name using its ID.

Example:

```http
DELETE /names/4
```

## 🧪 Swagger UI

FastAPI provides interactive API documentation through Swagger UI.

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI is currently being used to test the API endpoints during development.

## 💾 Current Data Storage

The project currently uses a Python dictionary as temporary in-memory storage:

```python
names_list = {
    1: "Ali",
    2: "Reza",
    3: "Amir"
}
```

Because the data is stored in memory, it will be reset whenever the application restarts.

Database integration will be added later in the learning process.

## 📚 Concepts Covered

* FastAPI basics
* Routing
* HTTP methods
* Query parameters
* Path parameters
* Request bodies
* JSON
* Pydantic
* CRUD operations
* API testing with Swagger UI
* HTTP status codes
* Error handling
* `HTTPException`
* Response models
* Pydantic validation


## 🔜 Next Steps

* Dependency Injection
* Better project structure
* Database integration
* Authentication and authorization
* Testing
* Docker
* Deployment

## 🚀 Running the Project

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python core/main.py
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 🎯 Purpose

This repository is a practical learning project for building a strong foundation in **FastAPI and Python backend development**.

The project will be continuously improved as new backend concepts are learned and implemented.
