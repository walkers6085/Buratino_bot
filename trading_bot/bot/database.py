import aiosqlite
from typing import Any, Dict, Optional

DB_PATH = "bot_data.db"


CREATE_USERS_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_seen TEXT,
        last_active TEXT
    );
    """
)

CREATE_EVENTS_TABLE = (
    """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_type TEXT,
        payload TEXT,
        timestamp TEXT
    );
    """
)


async def initialize_database() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_USERS_TABLE)
        await db.execute(CREATE_EVENTS_TABLE)
        await db.commit()


async def upsert_user(user_id: int, username: Optional[str], when_iso: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, username, first_seen, last_active)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
              username=excluded.username,
              last_active=excluded.last_active
            """,
            (user_id, username, when_iso, when_iso),
        )
        await db.commit()


async def insert_event(user_id: int, event_type: str, payload_json: str, when_iso: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO events (user_id, event_type, payload, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, event_type, payload_json, when_iso),
        )
        await db.commit()

