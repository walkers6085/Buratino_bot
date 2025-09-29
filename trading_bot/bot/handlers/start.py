from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..keyboards.reply import main_menu
from ..keyboards.inline import project_links
from ..analytics import track


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await track(
        user_id=message.from_user.id,
        username=message.from_user.username,
        event_type="bot_start",
        payload=None,
    )

    await message.answer(
        "Привет! Я помогу с обучением и данными по акциям Мосбиржи.",
        reply_markup=main_menu(),
    )

