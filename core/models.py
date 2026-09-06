from pydantic import BaseModel, Field, field_validator
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
class Name(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=20 )
    age: int = 18


    @field_validator("name")
    def validate_name(value: str):
        value = value.strip()
        if not value:
            raise ValueError("name cannot be empty")
        return value
    

class NameResponse(BaseModel):
    id: int 
    name: str
    age: int = Field(gt=0)
class Names(Base):
    __tablename__= "names"

    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(20))
    age: Mapped[int]= mapped_column(Integer())
