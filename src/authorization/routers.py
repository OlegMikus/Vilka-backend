from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.authorization.models import User_Pydantic, UserIn_Pydantic, Users
from src.authorization.utils.auth import AuthHandler

router = APIRouter()

auth_handler = AuthHandler()


class Status(BaseModel):
    message: str


class AuthDetails(BaseModel):
    username: str
    password: str


@router.post('/register', status_code=201)
async def register(user: UserIn_Pydantic):
    if await Users.get_or_none(username=user.username):
        raise HTTPException(status_code=400, detail='Username is taken')
    user.password = auth_handler.get_password_hash(user.password)
    print(user)
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.post('/login')
async def login(auth_details: AuthDetails):
    user = await Users.get_or_none(username=auth_details.username)
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_access_token(user.username)
    return {'token': token}


@router.get('/unprotected')
def unprotected():
    return {'hello': 'world'}


@router.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}


@router.get('/users', response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.put(
    '/user/{user_id}', response_model=User_Pydantic, responses={404: {'model': HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.delete('/user/{user_id}', response_model=Status, responses={404: {'model': HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    return Status(message=f'Deleted user {user_id}')
