from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: user_dependency, db: db_dependency, create_user_request: CreateUserRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    create_user_model = Users(
        email=create_user_request.email.lower(),
        username=create_user_request.username.lower(),
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role.lower(),
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

    return {
        "status": "Success",
        "detail": "User created Successfully."
    }


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.get('/all-users', status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    return db.query(Users).all()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()

    return {
        "status": "Success",
        "detail": "Password changed Successfully."
    }
