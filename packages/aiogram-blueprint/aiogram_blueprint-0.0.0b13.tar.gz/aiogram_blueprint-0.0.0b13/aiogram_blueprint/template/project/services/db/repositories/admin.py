import typing as t

from .base import BaseRepository
from ..models import AdminModel


class AdminRepository(BaseRepository[AdminModel]):
    model: t.Type[AdminModel] = AdminModel
