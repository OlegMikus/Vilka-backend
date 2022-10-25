from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.authorization.routers import router
from src.config.constants import DB_URL
from src.config.settings import TORTOISE_MODULES

app = FastAPI()

app.include_router(router)

register_tortoise(
    app,
    db_url=DB_URL,
    modules=TORTOISE_MODULES,
    generate_schemas=True,
    add_exception_handlers=True,
)
