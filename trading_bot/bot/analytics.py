import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .database import insert_event, upsert_user


async def track(user_id: int, username: Optional[str], event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
    now = datetime.now(timezone.utc).astimezone().isoformat()
    await upsert_user(user_id=user_id, username=username, when_iso=now)

    payload_json = json.dumps(payload or {}, ensure_ascii=False)
    # Важно: логирование асинхронно и не блокирует основной поток
    asyncio.create_task(insert_event(user_id=user_id, event_type=event_type, payload_json=payload_json, when_iso=now))

