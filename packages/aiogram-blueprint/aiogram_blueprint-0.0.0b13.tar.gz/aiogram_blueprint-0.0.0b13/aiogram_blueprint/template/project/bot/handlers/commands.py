from aiogram.types import Message

from ..utils import Localizer


async def start_command(message: Message, localizer: Localizer) -> None:
    text = await localizer("start", user=message.from_user)
    await message.answer(text)


# noinspection PyUnusedLocal
async def admin_command(message: Message) -> None: ...
