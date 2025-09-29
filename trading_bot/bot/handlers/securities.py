import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from aiogram import Router
from aiogram.types import Message

from ..api.moex import get_security_quote
from ..analytics import track


router = Router()

FUND_PATH = Path(__file__).resolve().parent.parent / "data" / "fundamental.json"


def _load_fundamental() -> dict:
    with open(FUND_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _should_ask_moex_poll(last_shown_iso: Optional[str]) -> bool:
    if not last_shown_iso:
        return True
    try:
        last_dt = datetime.fromisoformat(last_shown_iso)
    except Exception:
        return True
    now = datetime.now(timezone.utc).astimezone()
    return now.date() > last_dt.date()


@router.message(lambda m: m.text and m.text.startswith("/") is False and len(m.text.strip()) <= 6)
async def handle_ticker(message: Message) -> None:
    ticker = message.text.strip().upper()

    await track(
        user_id=message.from_user.id,
        username=message.from_user.username,
        event_type="ticker_requested",
        payload={"ticker": ticker},
    )

    quote = await get_security_quote(ticker)
    if not quote:
        await message.answer("Тикер не найден. Попробуйте, например, SBER.")
        return

    fund = _load_fundamental().get(ticker)
    fund_line = ""
    if fund:
        est = fund.get("fair_price_estimate")
        est_text = f" (~{est} ₽)" if est is not None else ""
        fund_line = f"\nДив. доходность: {fund.get('div_yield')}%. Оценка: акция недооценена{est_text}."

    text = (
        f"{quote['name']} ({quote['secid']})\n"
        f"Цена: {quote['price']}\n"
        f"Изм.: {quote['change_pct']}%\n"
        f"Объём: {quote['volume']}"
        f"{fund_line}"
    )
    await message.answer(text)

    # После первой котировки за день показываем опрос по MOEX
    # Простой вариант: всегда показывать, продакшн — хранить отметку в БД/кеше
    await track(
        user_id=message.from_user.id,
        username=message.from_user.username,
        event_type="moex_poll_shown",
        payload=None,
    )
    await message.answer("Кстати, куда, по-твоему, пойдёт MOEX на этой неделе?\nВыберите: 📈 Рост / 📉 Падение / ➡️ Боковик")

