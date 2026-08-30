from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI()

names_list = {
    1:'Ali',
    2:'Reza',
    3:'Amir'
}

class Name(BaseModel):
    id : int 
    name : str

@app.get("/")
async def root():
    return {'message' : 'hello from fast api'}


@app.get("/names")
async def search_item(id: int , name :str):
    return {
        'id': id ,
        'name': name
    }

@app.get("/names/{id}")
async def get_name(id : int):
    return {
        'id': id ,
        'name' : names_list[id]
    }

@app.post("/names")
async def creat_name(new_name: Name):
   names_list[new_name.id]= new_name.name
   return names_list

@app.delete("/names/{id}")
async def delete_name(id : int):
    del names_list[id]
    return names_list 

@app.put("/names/{id}")
async def put_name(id : int , name: str):
    names_list[id] = name
    return names_list

if __name__== "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)