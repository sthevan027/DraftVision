"""Redis cache layer for profiles and Riot API responses."""

from __future__ import annotations

import json
from typing import Any

from api.core.config import settings

# Lazy connection - only when Redis is configured
_redis: Any = None


def _get_redis():
    global _redis
    if _redis is None and settings.redis_url:
        try:
            import redis.asyncio as aioredis
            _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        except Exception:
            _redis = False  # Disabled on error
    return _redis if _redis else None


async def get_cached_profile(puuid: str) -> dict | None:
    """Return cached profile or None."""
    r = _get_redis()
    if not r:
        return None
    try:
        data = await r.get(f"profile:{puuid}")
        return json.loads(data) if data else None
    except Exception:
        return None


async def set_cached_profile(puuid: str, profile: dict, ttl_seconds: int = 300) -> None:
    """Cache profile with TTL (default 5 min)."""
    r = _get_redis()
    if not r:
        return
    try:
        await r.setex(
            f"profile:{puuid}",
            ttl_seconds,
            json.dumps(profile, default=str),
        )
    except Exception:
        pass


async def invalidate_profile(puuid: str) -> None:
    """Invalidate profile cache after sync."""
    r = _get_redis()
    if not r:
        return
    try:
        await r.delete(f"profile:{puuid}")
    except Exception:
        pass
