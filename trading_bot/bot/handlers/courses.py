import json
from pathlib import Path
from aiogram import Router
from aiogram.types import Message

from ..analytics import track


router = Router()

COURSES_PATH = Path(__file__).resolve().parent.parent / "data" / "courses.json"


def _load_courses() -> dict:
    with open(COURSES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@router.message(lambda m: m.text == "🎓 Курсы")
async def courses_entry(message: Message) -> None:
    courses = _load_courses()
    lesson_id, lesson = next(iter(courses.items()))

    await track(
        user_id=message.from_user.id,
        username=message.from_user.username,
        event_type="course_lesson_viewed",
        payload={"lesson_id": lesson_id},
    )

    text = f"{lesson['title']}\n\n{lesson['text']}\n\nТест: {lesson['test']['question']}\nВарианты: {', '.join(lesson['test']['options'])}\nОтветьте сообщением."
    await message.answer(text)


@router.message(lambda m: m.reply_to_message and "Тест:" in (m.reply_to_message.text or ""))
async def courses_test_answer(message: Message) -> None:
    courses = _load_courses()
    lesson_id, lesson = next(iter(courses.items()))
    answer = (message.text or "").strip()
    correct = answer == lesson["test"]["correct"]

    await track(
        user_id=message.from_user.id,
        username=message.from_user.username,
        event_type="course_test_submitted",
        payload={"lesson_id": lesson_id, "answer": answer, "correct": correct},
    )

    await message.answer("Верно!" if correct else "Неверно. Попробуйте ещё раз.")

