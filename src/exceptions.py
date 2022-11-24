from typing import Any, Optional, Dict

from fastapi import HTTPException
from starlette import status


class BadRequestError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UnauthorizedError(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: Any = 'Incorrect username or password',
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers={'WWW-Authenticate': 'Bearer'})
