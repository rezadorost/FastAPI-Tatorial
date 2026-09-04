from fastapi import APIRouter, HTTPException, Depends
from models import NameResponse , Name
router = APIRouter()


names_list = {
    1:'Ali',
    2:'Reza',
    3:'Amir'
}

async def get_name_id(id: int):
    return id

async def check_name_id(id: int= Depends(get_name_id)):
    if id not in names_list:
        raise HTTPException(
            status_code=404,
            detail= "Not Found"
        )
    return id
@router.get("/")
async def root():
    return {'message' : 'hello from fast api'}

@router.get("/names/{id}" , response_model= NameResponse)
async def get_name(id : int= Depends(check_name_id)):

    return {
        'id': id ,
        'name' : names_list[id]
    }

@router.post("/names", status_code=201)
async def creat_name(new_name: Name):
   names_list[new_name.id]= new_name.name
   return names_list

@router.delete("/names/{id}", status_code=204)
async def delete_name(id : int= Depends(check_name_id)):
    del names_list[id]
    return names_list 

@router.put("/names/{id}")
async def put_name(id : int, name: str= Depends(check_name_id)):
    names_list[id] = name
    return names_list
