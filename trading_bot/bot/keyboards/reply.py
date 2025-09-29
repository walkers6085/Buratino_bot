from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎓 Курсы"), KeyboardButton(text="📰 Данные по акциям")],
            [KeyboardButton(text="ℹ️ О проекте")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
    )

