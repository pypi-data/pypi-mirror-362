from aiogram.types import Message

from ..utils import Localizer


async def echo_message(message: Message, localizer: Localizer) -> None:
    text = await localizer("echo", message=message)
    await message.reply(text)
