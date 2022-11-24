import uuid
from fastapi import APIRouter, Depends
from starlette import status
from tortoise.contrib.pydantic import PydanticModel
from tortoise.expressions import Q

from src.db.models.friends import (
    Friendship,
    StatusCode,
)
from src.db.models.user import (
    User,
)
from src.pydantic_models.friends import (
    CreateFriendRequest,
    FriendshipPydantic,
    FriendshipPydanticQS,
)
from src.utils.auth import AuthHandler
from src.exceptions import NotFoundError

router = APIRouter()

auth_handler = AuthHandler()


@router.post('/create-friend-request')
async def create_friend_request(
        body: CreateFriendRequest,
        user: User = Depends(auth_handler)
) -> PydanticModel:
    friendship_data = {
        'addressee_id': body.friend_id,
        'requester': user,
        'specifier': user,
    }
    friendship_object = await Friendship.create(**friendship_data)
    return await FriendshipPydantic.from_tortoise_orm(friendship_object)


@router.get('/get-friendship-requests')
async def get_friendship_requests(user: User = Depends(auth_handler)) -> PydanticModel:
    friendship_objects = Friendship.objects.filter(addressee_id=str(user.id))

    return await FriendshipPydanticQS.from_queryset(friendship_objects)


@router.patch('/approve-friendship-request/{friendship_id}')
async def approve_friendship_request_by_id(friendship_id: uuid.UUID,
                                           user: User = Depends(auth_handler)) -> PydanticModel:
    friendship_request = await Friendship.objects.get_or_none(id=friendship_id, addressee_id=str(user.id))
    if not friendship_request:
        raise NotFoundError()

    friendship_request.status_code = StatusCode.ACCEPTED
    friendship_request.specifier = user
    await friendship_request.save()

    return await FriendshipPydantic.from_tortoise_orm(friendship_request)


@router.get('/get-friends-list')
async def get_friends_list(user: User = Depends(auth_handler)) -> PydanticModel:
    friendship_objects = Friendship.objects.filter(Q(requester_id=str(user.id)) | Q(addressee_id=str(user.id)),
                                                   status_code=StatusCode.ACCEPTED)

    return await FriendshipPydanticQS.from_queryset(friendship_objects)


@router.delete('/delete-friend/{friendship_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_friend(friendship_id: uuid.UUID, user: User = Depends(auth_handler)) -> PydanticModel:
    friendship_request = await Friendship.objects.get_or_none(
        Q(requester_id=str(user.id)) | Q(addressee_id=str(user.id)),
        id=friendship_id)
    if not friendship_request:
        raise NotFoundError()
    await friendship_request.delete()
    return {}


@router.patch('/block-friend/{friendship_id}')
async def block_friend(friendship_id: uuid.UUID, user: User = Depends(auth_handler)) -> PydanticModel:
    friendship_request = await Friendship.objects.get_or_none(
        Q(requester_id=str(user.id)) | Q(addressee_id=str(user.id)), id=friendship_id)
    if not friendship_request:
        raise NotFoundError()

    friendship_request.status_code = StatusCode.BLOCKED
    friendship_request.specifier = user
    await friendship_request.save()
    await friendship_request.delete()

    return await FriendshipPydantic.from_tortoise_orm(friendship_request)


@router.patch('/unblock-friend/{friendship_id}')
async def unblock_friend(friendship_id: uuid.UUID, user: User = Depends(auth_handler)) -> PydanticModel:
    friendship_request = await Friendship.get_or_none(specifier_id=str(user.id), id=friendship_id,
                                                      status_code=StatusCode.BLOCKED)
    if not friendship_request:
        raise NotFoundError()

    friendship_request.status_code = StatusCode.REQUESTED
    friendship_request.is_alive = True
    friendship_request.specifier = user
    await friendship_request.save()

    return await FriendshipPydantic.from_tortoise_orm(friendship_request)


@router.get('/get-blocked-friends')
async def get_blocked_friends(user: User = Depends(auth_handler)) -> PydanticModel:
    pass
