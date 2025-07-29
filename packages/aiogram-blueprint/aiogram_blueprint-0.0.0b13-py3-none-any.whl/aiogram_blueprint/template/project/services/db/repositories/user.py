import typing as t

from .base import BaseRepository
from ..models import UserModel


class UserRepository(BaseRepository[UserModel]):
    model: t.Type[UserModel] = UserModel
