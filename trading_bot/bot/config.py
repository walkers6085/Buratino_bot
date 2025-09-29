import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    bot_token: str
    log_level: str = "INFO"
    timezone: str = "Europe/Moscow"


def load_settings() -> Settings:
    # Lazy import to avoid hard dependency if .env is not used
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass

    return Settings(
        bot_token=os.getenv("BOT_TOKEN", ""),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        timezone=os.getenv("TZ", "Europe/Moscow"),
    )

