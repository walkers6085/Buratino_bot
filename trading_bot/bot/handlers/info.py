from aiogram import Router
from aiogram.types import Message

from ..keyboards.inline import project_links
from ..analytics import track


router = Router()


@router.message(lambda m: m.text == "ℹ️ О проекте")
async def info(message: Message) -> None:
    await track(
        user_id=message.from_user.id,
        username=message.from_user.username,
        event_type="info_opened",
        payload=None,
    )
    await message.answer("Полезные каналы:", reply_markup=project_links())

