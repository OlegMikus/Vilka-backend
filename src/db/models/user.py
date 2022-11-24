from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from src.db.models.base import BaseModel
from src.db.validators import EmailValidator


class User(BaseModel):
    """User model"""
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    email = fields.CharField(max_length=320, null=False, unique=True, validators=[EmailValidator(), ])
    password = fields.CharField(max_length=256, null=False)

    class Meta:
        table = 'user'
        ordering = ('email', )

    class PydanticMeta(BaseModel.PydanticMeta):
        exclude = BaseModel.PydanticMeta.exclude + ['password']


User_Pydantic = pydantic_model_creator(User, name='User', exclude=('password', ))
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', include=('password', ))
