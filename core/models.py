from pydantic import BaseModel, Field, field_validator
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

class PhoneNumberCreate(BaseModel):
    number: str = Field(min_length=11, max_length=11)

    @field_validator("number")
    def validate_number(value: str):
        if not value.isdigit():
            raise ValueError("phone number must contain only digits")
        return value


class PhoneNumberResponse(BaseModel):
    id: int
    number: str
    name_id: int

class NameResponse(BaseModel):
    id: int 
    name: str
    age: int = Field(gt=0)

class Names(Base):
    __tablename__= "names"

    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(20))
    age: Mapped[int]= mapped_column(Integer())

    phone_numbers = relationship("PhoneNumbers", back_populates="person")

class PhoneNumbers(Base):
    __tablename__= "phone_numbers"

    id: Mapped[int]= mapped_column(primary_key=True)
    number: Mapped[str]= mapped_column(String(11))
    name_id: Mapped[int]= mapped_column(ForeignKey("names.id"))

    person = relationship("Names", back_populates="phone_numbers")