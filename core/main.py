from pydantic import BaseModel , Field , field_validator
from fastapi import FastAPI , HTTPException
import uvicorn

app = FastAPI()

names_list = {
    1:'Ali',
    2:'Reza',
    3:'Amir'
}

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





@app.get("/")
async def root():
    return {'message' : 'hello from fast api'}



@app.get("/names/{id}" , response_model= NameResponse)
async def get_name(id : int):
    if id not in names_list:
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )

    return {
        'id': id ,
        'name' : names_list[id]
    }

@app.post("/names", status_code=201)
async def creat_name(new_name: Name):
   names_list[new_name.id]= new_name.name
   return names_list

@app.delete("/names/{id}", status_code=204)
async def delete_name(id : int):
    if id not in names_list:
        raise HTTPException(
            status_code=404 ,
            detail= "Not Found"
        )
    del names_list[id]
    return names_list 

@app.put("/names/{id}")
async def put_name(id : int , name: str):
    if id not in names_list:
        raise HTTPException(
            status_code=404 ,
            detail= "Not Found"
            )

    names_list[id] = name
    return names_list

if __name__== "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)