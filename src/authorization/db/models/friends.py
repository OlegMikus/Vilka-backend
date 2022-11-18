from enum import Enum
from typing import Iterable, Optional

from tortoise import BaseDBAsyncClient, Tortoise, fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from src.authorization.db.models.base import BaseModel


class StatusCode(str, Enum):
    REQUESTED = 'REQUESTED'
    ACCEPTED = 'ACCEPTED'
    DECLINED = 'DECLINED'
    BLOCKED = 'BLOCKED'


class Friendship(BaseModel):
    """Friendship model"""
    requester = fields.ForeignKeyField('user.User', related_name='friendship_to_requester_fk')
    addressee = fields.ForeignKeyField('user.User', related_name='friendship_to_addressee_fk')
    status_code: StatusCode = fields.CharEnumField(StatusCode, default=StatusCode.REQUESTED)
    specifier = fields.ForeignKeyField('user.User', related_name='friendship_status_specifier')

    class Meta:
        table = 'friendship'
        unique_together = ('requester', 'addressee',)

    async def save(
            self,
            using_db: Optional[BaseDBAsyncClient] = None,
            update_fields: Optional[Iterable[str]] = None,
            force_create: bool = False,
            force_update: bool = False,
    ) -> None:
        if self.requester == self.addressee:
            raise Exception
        await super(Friendship, self).save(using_db, update_fields, force_create, force_update)


Tortoise.init_models(['src.authorization.db.models.friends', 'src.authorization.db.models'], 'user')

Friendship_Pydantic = pydantic_model_creator(Friendship)
FriendshipQS_Pydantic = pydantic_queryset_creator(Friendship)
