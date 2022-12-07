from tortoise import fields
from src.db.models.base import BaseModel


class Photo(BaseModel):
    """Photo model"""
    user = fields.ForeignKeyField('user.User', on_delete=fields.CASCADE)
    destination = fields.CharField(max_length=256)
    name = fields.CharField(max_length=256)
    type = fields.CharField(max_length=128)
    size = fields.BigIntField()
    hash = fields.CharField(max_length=512)

    class Meta:
        table = 'photo'
        ordering = ('name', )
