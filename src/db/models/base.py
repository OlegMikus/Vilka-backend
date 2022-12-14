import uuid
from typing import Optional

from tortoise import BaseDBAsyncClient, fields, models

from src.db.managers import AliveOnlyManager


class BaseModel(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_alive = fields.BooleanField(default=True)

    objects = AliveOnlyManager()

    class Meta:
        abstract = True

    class PydanticMeta:
        exclude = [
            'is_alive',
            'created_at',
            'updated_at',
        ]

    async def delete(self, using_db: Optional[BaseDBAsyncClient] = None) -> None:
        self.is_alive = False
        await self.save()
