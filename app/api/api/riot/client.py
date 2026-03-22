"""Riot API client abstraction for V1 vertical slice."""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol
from urllib.parse import quote

import time

import httpx

from api.core.config import settings

MAX_RETRIES = 3
RETRY_DELAY_BASE = 1.0

logger = logging.getLogger(__name__)

# Platform -> regional routing for account-v1 and match-v5
PLATFORM_TO_REGION: dict[str, str] = {
    "br1": "americas",
    "na1": "americas",
    "la1": "americas",
    "la2": "americas",
    "kr": "asia",
    "jp1": "asia",
    "euw1": "europe",
    "eun1": "europe",
    "tr1": "europe",
    "ru": "europe",
    "me1": "europe",
    "oc1": "sea",
    "ph2": "sea",
    "sg2": "sea",
    "th2": "sea",
    "tw2": "sea",
    "vn2": "sea",
}

DEFAULT_REGION = "americas"


@dataclass
class RiotPlayer:
    puuid: str
    game_name: str
    tag_line: str
    summoner_name: str
    region: str


@dataclass
class RiotMatchStats:
    match_id: str
    queue: str
    played_at: datetime
    game_duration_minutes: float
    win: bool
    kills: int
    deaths: int
    assists: int
    cs: int
    vision_score: int


class RiotClientProtocol(Protocol):
    """Protocol for Riot API client."""

    def get_player(self, game_name: str, tag_line: str, region: str) -> RiotPlayer: ...
    def get_recent_ranked_matches(
        self, puuid: str, count: int, region: str
    ) -> list[RiotMatchStats]: ...


class MockRiotClient:
    """Deterministic mock for tests and dev without API key."""

    def get_player(self, game_name: str, tag_line: str, region: str = "br1") -> RiotPlayer:
        raw = f"{game_name}#{tag_line}".encode("utf-8")
        puuid = hashlib.sha256(raw).hexdigest()
        return RiotPlayer(
            puuid=puuid,
            game_name=game_name,
            tag_line=tag_line,
            summoner_name=f"{game_name}#{tag_line}",
            region=region,
        )

    def get_recent_ranked_matches(
        self, puuid: str, count: int = 20, region: str = "br1"
    ) -> list[RiotMatchStats]:
        now = datetime.now(timezone.utc)
        matches: list[RiotMatchStats] = []
        for index in range(count):
            base = int(hashlib.md5(f"{puuid}:{index}".encode("utf-8")).hexdigest()[:8], 16)
            duration = 22 + (base % 16)
            deaths = 1 + (base % 9)
            kills = 2 + (base % 14)
            assists = 1 + ((base // 3) % 17)
            cs = 130 + (base % 140)
            vision_score = 10 + (base % 30)
            matches.append(
                RiotMatchStats(
                    match_id=f"BR1_{puuid[:10]}_{index}",
                    queue="RANKED_SOLO_5x5",
                    played_at=now - timedelta(days=index),
                    game_duration_minutes=float(duration),
                    win=(base % 2 == 0),
                    kills=kills,
                    deaths=deaths,
                    assists=assists,
                    cs=cs,
                    vision_score=vision_score,
                )
            )
        return matches


class RealRiotClient:
    """Real Riot API client with account-v1 and match-v5."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or settings.riot_api_key
        self._timeout = httpx.Timeout(30.0)

    def _headers(self) -> dict[str, str]:
        return {"X-Riot-Token": self._api_key}

    def _region(self, platform: str) -> str:
        return PLATFORM_TO_REGION.get(platform.lower(), DEFAULT_REGION)

    def _base_url(self, platform: str, use_region: bool = True) -> str:
        if use_region:
            r = self._region(platform)
            return f"https://{r}.api.riotgames.com"
        return f"https://{platform.lower()}.api.riotgames.com"

    def _request_with_retry(self, method: str, url: str, **kwargs) -> httpx.Response:
        last_err: Exception | None = None
        resp: httpx.Response | None = None
        with httpx.Client(timeout=self._timeout) as client:
            for attempt in range(MAX_RETRIES):
                try:
                    resp = client.request(method, url, headers=self._headers(), **kwargs)
                    if resp.status_code == 429:
                        delay = int(resp.headers.get("Retry-After", RETRY_DELAY_BASE * (2**attempt)))
                        logger.warning("Rate limited (429), retry after %ds", delay)
                        time.sleep(delay)
                        continue
                    if resp.status_code == 503:
                        delay = RETRY_DELAY_BASE * (2**attempt)
                        logger.warning("Service unavailable (503), retry in %.1fs", delay)
                        time.sleep(delay)
                        continue
                    return resp
                except httpx.HTTPError as e:
                    last_err = e
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY_BASE * (2**attempt))
        if last_err:
            raise last_err
        return resp  # type: ignore[return-value]

    def get_player(self, game_name: str, tag_line: str, region: str = "br1") -> RiotPlayer:
        base = self._base_url(region)
        url = f"{base}/riot/account/v1/accounts/by-riot-id/{quote(game_name)}/{quote(tag_line)}"
        resp = self._request_with_retry("GET", url)
        resp.raise_for_status()
        data = resp.json()
        return RiotPlayer(
            puuid=data["puuid"],
            game_name=data["gameName"],
            tag_line=data["tagLine"],
            summoner_name=f"{data['gameName']}#{data['tagLine']}",
            region=region,
        )

    def get_recent_ranked_matches(self, puuid: str, count: int = 20, region: str = "br1") -> list[RiotMatchStats]:
        region_routing = self._region(region)
        base = self._base_url(region)
        ids_url = f"{base}/lol/match/v5/matches/by-puuid/{puuid}/ids"
        resp = self._request_with_retry(
            "GET", ids_url, params={"count": count, "type": "ranked"}
        )
        resp.raise_for_status()
        match_ids = resp.json()[:count]
        if not match_ids:
            return []

        matches: list[RiotMatchStats] = []
        for match_id in match_ids:
            try:
                stats = self._fetch_match_stats(base, match_id, puuid)
                if stats:
                    matches.append(stats)
            except Exception as e:
                logger.warning("Failed to fetch match %s: %s", match_id, e)
        return matches

    def _fetch_match_stats(self, base_url: str, match_id: str, puuid: str) -> RiotMatchStats | None:
        url = f"{base_url}/lol/match/v5/matches/{match_id}"
        resp = self._request_with_retry("GET", url)
        resp.raise_for_status()
        data = resp.json()
        duration_sec = data.get("info", {}).get("gameDuration", 0)
        duration_min = duration_sec / 60.0 if duration_sec else 20.0
        queue = data.get("info", {}).get("queueId", 420)
        queue_str = "RANKED_SOLO_5x5" if queue == 420 else f"QUEUE_{queue}"
        ts = data.get("info", {}).get("gameStartTimestamp", 0)
        played_at = datetime.fromtimestamp(ts / 1000, tz=timezone.utc) if ts else datetime.now(timezone.utc)

        participants = data.get("info", {}).get("participants", [])
        for p in participants:
            if p.get("puuid") == puuid:
                win = p.get("win", False)
                kills = p.get("kills", 0)
                deaths = p.get("deaths", 0)
                assists = p.get("assists", 0)
                cs = p.get("totalMinionsKilled", 0) + p.get("neutralMinionsKilled", 0)
                vision_score = p.get("visionScore", 0)
                return RiotMatchStats(
                    match_id=match_id,
                    queue=queue_str,
                    played_at=played_at,
                    game_duration_minutes=duration_min,
                    win=win,
                    kills=kills,
                    deaths=deaths,
                    assists=assists,
                    cs=cs,
                    vision_score=vision_score,
                )
        return None


def get_riot_client() -> RiotClientProtocol:
    """Return real client if API key is set, else mock."""
    if settings.riot_api_key:
        return RealRiotClient()
    return MockRiotClient()
