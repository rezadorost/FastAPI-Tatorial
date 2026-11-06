from pydantic import BaseModel, Field, field_validator, ConfigDict
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class UserUpdate(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=20
    )
    email: str | None = None


class PhoneNumberCreate(BaseModel):
    number: str = Field(min_length=11, max_length=11)

    @field_validator("number")
    @classmethod
    def validate_number(cls, value: str):
        if not value.isdigit():
            raise ValueError("phone number must contain only digits")
        return value


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: str
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str
    role: str

class PhoneNumberResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)


    id: int
    number: str

class AdminDashboardResponse(BaseModel):
    message: str
    user: str

class PhoneNumbers(Base):
    __tablename__ = "phone_numbers"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(11))

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user = relationship(
        "Users",
        back_populates="phone_numbers"
    )

class Users(Base):
    __tablename__= "users"
    id: Mapped[int]= mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    phone_numbers = relationship("PhoneNumbers", back_populates="user", cascade="all, delete-orphan")
