import typing as t

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from ...context import Context
from ...services.db.models import UserModel
from ...services.db.unitofwork import UnitOfWork


class DbSessionMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: t.Callable[
                [TelegramObject, t.Dict[str, t.Any]],
                t.Awaitable[t.Any]
            ],
            event: TelegramObject,
            data: t.Dict[str, t.Any],
    ) -> t.Optional[t.Any]:
        user: t.Optional[User] = data.get("event_from_user")
        ctx: t.Optional[Context] = data.get("ctx")

        if not ctx:
            raise RuntimeError("Context is not available in middleware data")
        if not hasattr(ctx, "session_factory") or not ctx.session_factory:
            raise RuntimeError("Database session factory is not configured in context")

        uow = UnitOfWork(ctx.session_factory)

        async with uow:
            if user and not user.is_bot:
                user_model = UserModel(
                    id=user.id,
                    language_code=user.language_code,
                    full_name=user.full_name,
                    username=user.username,
                )
                if not await uow.user_repo.exists(id=user.id):
                    await uow.user_repo.create(**user_model.model_dump())
                else:
                    await uow.user_repo.update(
                        user.id,
                        **user_model.model_dump(
                            exclude=[UserModel.get_pk_column()]
                        ),
                    )

            data["uow"] = uow
            return await handler(event, data)
