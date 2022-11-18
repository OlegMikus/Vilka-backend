import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status
from tortoise import Tortoise
from tortoise.contrib.pydantic import PydanticModel

from src.authorization.db.models.friends import (Friendship,
                                                 Friendship_Pydantic,
                                                 FriendshipQS_Pydantic)
from src.authorization.db.models.user import (User, User_Pydantic,
                                              UserIn_Pydantic)
from src.authorization.utils.auth import AuthHandler

router = APIRouter()

auth_handler = AuthHandler()


class CreateFriendRequest(BaseModel):
    friend_id: uuid.UUID


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


class Token(BaseModel):
    access_token: str
    refresh_token: str


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_handler.authenticate_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return auth_handler.encode_token_pair(str(user.id))


@router.post('/create-friend-request')
async def create_friend_request(
        body: CreateFriendRequest,
        user: User = Depends(auth_handler.get_user)
) -> PydanticModel:

    friendship_data = {
        'addressee_id': body.friend_id,
        'requester_id': user.id,
        'specifier_id': user.id,
    }
    friendship_object = await Friendship.create(**friendship_data)
    return await Friendship_Pydantic.from_tortoise_orm(friendship_object)


@router.get('/get-friendship-requests')
async def get_friendship_requests(
        user: User = Depends(auth_handler.get_user)
) -> PydanticModel:
    Tortoise.init_models(['src.authorization.db.models'], 'user')
    friendship_objects = Friendship.objects.filter(addressee_id=str(user.id))

    return await FriendshipQS_Pydantic.from_queryset(friendship_objects)
