from fastapi import APIRouter, HTTPException, Depends
from .models import NameResponse, Name, Names
from .models import PhoneNumberCreate, PhoneNumbers, PhoneNumberResponse
from sqlalchemy.orm import Session
from .database import get_db

router = APIRouter()

async def check_name_id(
        id: int,
        db: Session = Depends(get_db)
):
    name = db.get(Names, id)
    if name is None:
        raise HTTPException(
            status_code=404,
            detail= "Not Found"
        )
    return name
@router.get("/")
async def root():
    return {'message' : 'hello from fast api'}

@router.get("/names/{id}" , response_model= NameResponse)
async def get_name(name: Names = Depends(check_name_id)):

    return {
        "id": name.id,
        "name": name.name,
        "age" : name.age
        }

@router.post("/names", status_code=201)
async def creat_name(
    new_name: Name,
    db: Session = Depends(get_db)
    ):
    db_name = Names(id= new_name.id,
                   name= new_name.name,
                   age= new_name.age
                   )
    db.add(db_name)
    db.commit()



    return db_name


@router.delete("/names/{id}", status_code=204)
async def delete_name(
    db: Session = Depends(get_db),
    name: Names = Depends(check_name_id)
    ):
    db.delete(name)
    db.commit()

@router.put("/names/{id}")
async def put_name(
    new_name: Name,
    db: Session = Depends(get_db),
    name: Names = Depends(check_name_id)
    ):
    name.name = new_name.name
    name.age = new_name.age
    db.commit()

    return name

@router.post(
        "/names/{name_id}/phone-numbers",
        status_code=201,
        response_model=PhoneNumberResponse
        )
async def add_phonenumbers(
    number: PhoneNumberCreate,
    name_id: int,
    db: Session = Depends(get_db)
    ):
    name = db.get(Names, name_id)
    if name is None:
        raise HTTPException(
            status_code=404,
            detail="id Not Found"
        )
    db_phone = PhoneNumbers(
        number=number.number,
        name_id = name_id
    )
    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)

    
    return db_phone

@router.get("/names/{name_id}/phone-numbers", response_model=list[PhoneNumberResponse])
async def get_phonenumbers(
    name_id: int,
    db: Session = Depends(get_db) 
):
    name = db.get(Names, name_id)
    if name is None:
        raise HTTPException(
            status_code=404,
            detail="id Not Found"
        )
    return name.phone_numbers