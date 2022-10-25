from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

TORTOISE_ORM = {
    "connections": {"default": "postgres://postgres:password@localhost:5432/vilka_db"},
    "apps": {
        "models": {
            "models": ["src.authorization.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    db_url="postgres://postgres:password@localhost:5432/vilka_db",
    modules={"models": ["src.authorization.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
