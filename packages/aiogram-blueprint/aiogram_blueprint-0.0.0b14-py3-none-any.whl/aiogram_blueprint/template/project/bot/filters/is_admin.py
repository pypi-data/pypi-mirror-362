from typing import Any, Dict, Union, Optional

from aiogram.filters import Filter
from aiogram.types import TelegramObject, User

from ...config import DEV_ID, ADMIN_IDS
from ...services.db.unitofwork import UnitOfWork


class IsAdmin(Filter):

    async def __call__(
            self,
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Union[bool, Dict[str, Any]]:
        user: Optional[User] = data.get("event_from_user")
        uow: Optional[UnitOfWork] = data.get("uow")

        if not user or user.is_bot:
            return False
        if user.id == DEV_ID or user.id in ADMIN_IDS:
            return True
        if uow is not None:
            return await uow.admin_repo.exists(user_id=user.id)

        return False
