import asyncio
import aiohttp
from functools import lru_cache
from typing import Any, Dict, Optional


MOEX_URL = (
    "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json?iss.only=marketdata,securities"
)


async def _fetch_json(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


@lru_cache(maxsize=64)
def _cache_key_60s() -> int:
    # Ключ меняется раз в 60 секунд
    return int(asyncio.get_event_loop().time() // 60)


async def get_security_quote(ticker: str) -> Optional[Dict[str, Any]]:
    _ = _cache_key_60s()
    ticker = ticker.strip().upper()
    async with aiohttp.ClientSession() as session:
        data = await _fetch_json(session, MOEX_URL)

    securities_cols = data.get("securities", {}).get("columns", [])
    securities_data = data.get("securities", {}).get("data", [])
    market_cols = data.get("marketdata", {}).get("columns", [])
    market_data = data.get("marketdata", {}).get("data", [])

    try:
        secid_idx = securities_cols.index("SECID")
        shortname_idx = securities_cols.index("SHORTNAME")
    except ValueError:
        return None

    secid_to_name: Dict[str, str] = {}
    for row in securities_data:
        secid = row[secid_idx]
        shortname = row[shortname_idx]
        secid_to_name[secid] = shortname

    try:
        last_idx = market_cols.index("LAST")
        change_idx = market_cols.index("LASTTOPREVPRICE")
        vol_idx = market_cols.index("VOLUME")
        secid_m_idx = market_cols.index("SECID")
    except ValueError:
        return None

    for row in market_data:
        if row[secid_m_idx] == ticker:
            return {
                "secid": ticker,
                "name": secid_to_name.get(ticker, ticker),
                "price": row[last_idx],
                "change_pct": row[change_idx],
                "volume": row[vol_idx],
            }
    return None

