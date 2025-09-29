import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from .config import load_settings
from .database import initialize_database
from .handlers.start import router as start_router
from .handlers.info import router as info_router
from .handlers.courses import router as courses_router
from .handlers.securities import router as securities_router


async def main() -> None:
    settings = load_settings()
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN не задан в .env")

    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))

    await initialize_database()

    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=None))
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(courses_router)
    dp.include_router(securities_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

