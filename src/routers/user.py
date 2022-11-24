from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.pydantic import PydanticModel

from src.db.models.user import UserIn_Pydantic, User, User_Pydantic
from src.exceptions import UnauthorizedError, BadRequestError
from src.pydantic_models.friends import Token
from src.utils.auth import AuthHandler

router = APIRouter()

auth_handler = AuthHandler()


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_handler.authenticate_user(form_data)
    if not user:
        raise UnauthorizedError()
    return auth_handler.encode_token_pair(str(user.id))


@router.post('/register', status_code=201)
async def register(user: UserIn_Pydantic) -> PydanticModel:
    if await User.get_or_none(username=user.username):
        raise BadRequestError(detail='Username is taken')
    user.password = auth_handler.get_password_hash(user.password)
    user_obj = await User.create(**user.dict(exclude_unset=True))

    return await User_Pydantic.from_tortoise_orm(user_obj)
