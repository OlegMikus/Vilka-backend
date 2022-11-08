from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.contrib.pydantic import PydanticModel

from src.authorization.db.models.user import (User, User_Pydantic,
                                              UserIn_Pydantic)
from src.authorization.utils.auth import AuthHandler

router = APIRouter()

auth_handler = AuthHandler()


class Status(BaseModel):
    message: str


class AuthDetails(BaseModel):
    username: str
    password: str


@router.post('/register', status_code=201)
async def register(user: UserIn_Pydantic) -> PydanticModel:
    if await User.get_or_none(username=user.username):
        raise HTTPException(status_code=400, detail='Username is taken')
    user.password = auth_handler.get_password_hash(user.password)
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.post('/login')
async def login(auth_details: AuthDetails) -> Dict[str, str]:
    user = await User.get_or_none(username=auth_details.username)
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.password)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_access_token(user.username)
    return {'token': token}


@router.patch('/user/', response_model=User_Pydantic, responses={404: {'model': HTTPNotFoundError}})
async def update_user(user: UserIn_Pydantic, username=Depends(auth_handler.auth_wrapper)) -> PydanticModel:
    user_by_name = await User.get_or_none(username=username)
    if not user_by_name:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    user.password = auth_handler.get_password_hash(user.password)
    await User.filter(username=username).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(username=username))


@router.delete("/user/{user_id}", response_model=Status, responses={404: {'model': HTTPNotFoundError}})
async def delete_user(user_id: int) -> Status:
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    return Status(message=f'Deleted user {user_id}')
