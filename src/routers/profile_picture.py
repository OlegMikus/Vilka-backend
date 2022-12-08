import os

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import Response

from src.db.models.user import User
from src.utils.auth import AuthHandler

router = APIRouter()

auth_handler = AuthHandler()


@router.get('/download-picture/')
async def create_upload_file():
    return Response(media_type='application/force-download',
                    headers={'Content-Disposition': f'attachment; filename:"CV_Oleg_Mikus.pdf"',
                             'X-Accel-Redirect': '/storage/CV_Oleg_Mikus.pdf',
                             }
                    )


@router.get('/get-all-photos/')
async def create_upload_file(file: UploadFile, user: User = Depends(auth_handler)):
    with open(f"./storage/{user.id}/{file.filename}", 'wb') as files:
        files.write(await file.read())
    return {'filename': file.filename}


@router.get('/get-photo/')
async def create_upload_file(file: UploadFile, user: User = Depends(auth_handler)):
    with open(f"./storage/{user.id}/{file.filename}", 'wb') as files:
        files.write(await file.read())
    return {'filename': file.filename}


@router.post('/upload-photo/')
async def create_upload_file(file: UploadFile, user: User = Depends(auth_handler)):

    os.makedirs(f'./storage/{user.id}', 0o777, exist_ok=True)
    with open(f"./storage/{user.id}/{file.filename}", 'wb') as files:
        files.write(await file.read())
    print(dir(file))
    return {'filename': file.filename}
