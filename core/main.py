
from fastapi import FastAPI
from .routes import router
from .database import engine, Base
from . import models


tags_metadata = [
    {
        "name": "Phone Numbers",
        "description": "Operations for managing user phone numbers.",
    },
    {
        "name": "Users",
        "description": "User registration, login, and profile operations.",
    },
    {
        "name": "Admin",
        "description": "Administrative operations for managing users and permissions.",
    },
]


app = FastAPI(
    title="FastAPI Tutorial API",
    description="""
    A RESTful API built with FastAPI and SQLAlchemy.

    ## Features

    - User registration and login
    - JWT-based authentication
    - Role-based access control (RBAC)
    - User management
    - Phone number management
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.include_router(router)

Base.metadata.create_all(bind=engine)
