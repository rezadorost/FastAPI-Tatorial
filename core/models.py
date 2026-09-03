from pydantic import BaseModel , Field , field_validator

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