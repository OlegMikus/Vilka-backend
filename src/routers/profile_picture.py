from fastapi import APIRouter, Depends, UploadFile

from src.db.models.user import User
from src.utils.auth import AuthHandler

router = APIRouter()

auth_handler = AuthHandler()


@router.post('/uploadfile/')
async def create_upload_file(file: UploadFile, user: User = Depends(auth_handler)):
    with open(file.filename, 'wb') as files:
        files.write(await file.read())
    return {'filename': file.filename}
