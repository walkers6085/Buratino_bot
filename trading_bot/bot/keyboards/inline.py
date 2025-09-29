from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def project_links() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎓 Обучение", url="https://t.me/edu_channel_placeholder")],
            [InlineKeyboardButton(text="📰 Основной", url="https://t.me/main_channel_placeholder")],
            [InlineKeyboardButton(text="💰 Облигации", url="https://t.me/bonds_channel_placeholder")],
        ]
    )

