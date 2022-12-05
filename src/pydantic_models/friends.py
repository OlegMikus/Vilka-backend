import uuid

from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from src.db.models import Friendship


class CreateFriendRequest(BaseModel):
    friend_id: uuid.UUID


class AuthDetails(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


Tortoise.init_models(['src.db.models.friends', 'src.db.models.user'], 'user')

FriendshipPydantic = pydantic_model_creator(Friendship)
FriendshipPydanticQS = pydantic_queryset_creator(Friendship, exclude=(
    'requester',
    'specifier',
    'addressee',
    'id',
    '',
    ))
