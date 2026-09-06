from fastapi import FastAPI
from .routes import router
from .database import engine, Base
from . import models

app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)