import os
from datetime import datetime, timedelta
from typing import Dict

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from src.db.models.user import User


class AuthHandler:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/token')
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    secret = os.environ.get('SECRET_KEY', 'aaaa')

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def __encode_access_token(self, user_id: str) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=60),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def __encode_refresh_token(self, user_id: str) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def encode_token_pair(self, user_id: str) -> Dict[str, str]:
        return {
            'access_token': self.__encode_access_token(user_id),
            'refresh_token': self.__encode_refresh_token(user_id),
        }

    def __decode_token(self, token: str = Depends(oauth2_scheme)) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    async def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> User | bool:
        user = await User.get_or_none(username=form_data.username)
        if not user:
            return False
        if not self.verify_password(form_data.password, user.password):
            return False
        return user

    async def get_user(self, token: str = Depends(oauth2_scheme)) -> User:
        user = await User.get(id=self.__decode_token(token))
        return user

    async def __call__(self, token: str = Depends(oauth2_scheme)) -> User:
        return await self.get_user(token)
