import re

from tortoise.exceptions import ValidationError
from tortoise.validators import Validator


class EmailValidator(Validator):

    def __call__(self, value: str) -> None:
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if not re.match(regex, value.lower()):
            raise ValidationError(f"Value '{value}' is invalid email")
