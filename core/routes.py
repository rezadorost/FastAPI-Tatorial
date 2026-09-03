from fastapi import APIRouter, HTTPException
from models import NameResponse , Name
router = APIRouter()


names_list = {
    1:'Ali',
    2:'Reza',
    3:'Amir'
}

@router.get("/")
async def root():
    return {'message' : 'hello from fast api'}

@router.get("/names/{id}" , response_model= NameResponse)
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

@router.post("/names", status_code=201)
async def creat_name(new_name: Name):
   names_list[new_name.id]= new_name.name
   return names_list

@router.delete("/names/{id}", status_code=204)
async def delete_name(id : int):
    if id not in names_list:
        raise HTTPException(
            status_code=404 ,
            detail= "Not Found"
        )
    del names_list[id]
    return names_list 

@router.put("/names/{id}")
async def put_name(id : int , name: str):
    if id not in names_list:
        raise HTTPException(
            status_code=404 ,
            detail= "Not Found"
            )

    names_list[id] = name
    return names_list
