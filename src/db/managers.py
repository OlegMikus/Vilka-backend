from tortoise import Model
from tortoise.manager import Manager
from tortoise.queryset import QuerySet


class AliveOnlyManager(Manager):
    def get_queryset(self) -> QuerySet[Model]:
        return super(AliveOnlyManager, self).get_queryset().filter(is_alive=True)
