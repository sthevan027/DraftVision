"""Riot API client abstraction for V1 vertical slice."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


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


class RiotClient:
    """Deterministic local client for development and tests.

    It emulates Riot responses without requiring external network access.
    """

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

    def get_recent_ranked_matches(self, puuid: str, count: int = 20) -> list[RiotMatchStats]:
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
