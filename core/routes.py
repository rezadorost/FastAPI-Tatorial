from fastapi import APIRouter, HTTPException, Depends, status
from .models import Users, UserUpdate
from .models import (PhoneNumberCreate,
                     PhoneNumbers,
                     PhoneNumberResponse,
                     UserCreate,
                     UserResponse, AdminDashboardResponse)
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user, hash_password, verify_password
from .auth import create_access_token, require_permission
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get("/")
async def root():
    return {'message' : 'hello from fast api'}

@router.post(
    "/phone-numbers",
    status_code=201,
    response_model=PhoneNumberResponse
)
def add_phonenumber(
    number: PhoneNumberCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    db_phone = PhoneNumbers(
        number=number.number,
        user_id=current_user.id
    )

    db.add(db_phone)
    db.commit()
    db.refresh(db_phone)

    return db_phone


@router.get(
    "/phone-numbers",
    response_model=list[PhoneNumberResponse]
)
def get_phonenumbers(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return db.query(PhoneNumbers).filter(
        PhoneNumbers.user_id == current_user.id
    ).all()


@router.put(
    "/phone-numbers/{phone_id}",
    response_model=PhoneNumberResponse,
    summary="Update a phone number",
    description="""
    First, call GET /phone-numbers to retrieve your phone numbers.
    Find the ID of the phone number you want to update.
    Then use that ID in this endpoint's URL.
    """
)
def update_phonenumber(
    phone_id: int,
    number: PhoneNumberCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    phone = db.get(PhoneNumbers, phone_id)

    if phone is None:
        raise HTTPException(
            status_code=404,
            detail="Phone number not found"
        )

    if phone.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't own this phone number"
        )

    phone.number = number.number

    db.commit()
    db.refresh(phone)

    return phone


@router.delete(
    "/phone-numbers/{phone_id}",
    status_code=204
)
def delete_phonenumber(
    phone_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    phone = db.get(PhoneNumbers, phone_id)

    if phone is None:
        raise HTTPException(
            status_code=404,
            detail="Phone number not found"
        )

    if phone.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't own this phone number"
        )

    db.delete(phone)
    db.commit()

@router.get("/users/me")
def read_users_me(current_user: Users = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

@router.post("/users/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_username = db.query(Users).filter(
        Users.username == user.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    existing_email = db.query(Users).filter(
        Users.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    new_user = Users(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

    db.refresh(new_user)
    return new_user

@router.post("/users/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.username == form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/admin", response_model=AdminDashboardResponse)
def admin_dashboard(
                    admin_user: Users = Depends(
                        require_permission("users:read")
                    )
    ):
    return {
        "message": "welcome to the admin dashboard",
        "user": admin_user.username
    }

@router.get(
    "/admin/users",
    response_model=list[UserResponse]
)
def get_all_users(
    admin_user: Users = Depends(
        require_permission("users:read")
    ),
    db: Session = Depends(get_db)
):
    return db.query(Users).all()

@router.get(
    "/admin/users/{user_id:int}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    admin_user: Users = Depends(
        require_permission("users:read")
    ),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(
        Users.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put("/admin/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_permission("users:update"))
):
    user = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user_data.model_dump(exclude_unset=True)

    if "username" in update_data and update_data["username"] is not None:
        existing_username = db.query(Users).filter(
            Users.username == update_data["username"],
            Users.id != user_id
        ).first()

        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )

    if "email" in update_data and update_data["email"] is not None:
        existing_email = db.query(Users).filter(
            Users.email == update_data["email"],
            Users.id != user_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

    db.refresh(user)
    return user

@router.delete(
    "/admin/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    admin_user: Users = Depends(
        require_permission("users:delete")
    ),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(
        Users.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == admin_user.id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete their own account"
        )

    db.delete(user)
    db.commit()

@router.get(
    "/admin/users/admins",
    response_model=list[UserResponse]
)
def get_admins(
    admin_user: Users = Depends(
        require_permission("admins:read")
    ),
    db: Session = Depends(get_db)
):
    admins  = db.query(Users).filter(Users.role == "admin").all()

    return admins

@router.patch(
    "/admin/users/{user_id}/promote",
    response_model=UserResponse
)
def promote_user(
    user_id: int,
    admin_user: Users = Depends(
        require_permission("users:promote")
    ),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(
        Users.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role == "admin":
        raise HTTPException(
            status_code=400,
            detail="User is already an admin"
        )

    user.role = "admin"

    db.commit()
    db.refresh(user)

    return user

@router.patch(
    "/admin/users/{user_id}/demote",
    response_model=UserResponse
)
def demote_user(
    user_id: int,
    admin_user: Users = Depends(
        require_permission("users:demote")
    ),
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter(
        Users.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role == "user":
        raise HTTPException(
            status_code=400,
            detail="User is already an user"
        )

    admin_count = db.query(func.count(Users.id)).filter(
        Users.role == "admin").scalar()

    if admin_count <= 1:
        raise HTTPException(
            status_code=400,
            detail= "Cannot demote the last admin!"
        )

    user.role = "user"

    db.commit()
    db.refresh(user)

    return user
