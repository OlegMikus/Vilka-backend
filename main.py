from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.config.constants import DB_URL
from src.config.settings import TORTOISE_MODULES
from src.routers.friendship import router as friendship_router
from src.routers.profile_picture import router as profile_picture_router
from src.routers.user import router as user_router

app = FastAPI()

app.include_router(prefix='/user', router=user_router)
app.include_router(prefix='/friend', router=friendship_router)
app.include_router(prefix='/profile', router=profile_picture_router)

register_tortoise(
    app,
    db_url=DB_URL,
    modules=TORTOISE_MODULES,
    generate_schemas=True,
    add_exception_handlers=True,
)
