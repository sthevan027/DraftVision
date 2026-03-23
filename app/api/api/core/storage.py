"""In-memory persistence and shared record types for the V1 vertical slice."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class PlayerRecord:
    puuid: str
    game_name: str
    tag_line: str
    summoner_name: str
    region: str
    updated_at: datetime


@dataclass
class MatchRecord:
    match_id: str
    queue: str
    game_duration_minutes: float
    played_at: datetime


@dataclass
class PlayerMatchStatsRecord:
    puuid: str
    match_id: str
    win: bool
    kills: int
    deaths: int
    assists: int
    cs: int
    vision_score: int
    game_duration_minutes: float


class InMemoryStore:
    def __init__(self) -> None:
        self.players: dict[str, PlayerRecord] = {}
        self.matches: dict[str, MatchRecord] = {}
        self.player_match_stats: dict[tuple[str, str], PlayerMatchStatsRecord] = {}

    def upsert_player(self, player: PlayerRecord) -> None:
        self.players[player.puuid] = player

    def upsert_match(self, match: MatchRecord) -> None:
        self.matches[match.match_id] = match

    def upsert_player_match_stats(self, stats: PlayerMatchStatsRecord) -> None:
        key = (stats.puuid, stats.match_id)
        self.player_match_stats[key] = stats

    def list_player_stats(self, puuid: str) -> list[PlayerMatchStatsRecord]:
        return [value for (p, _), value in self.player_match_stats.items() if p == puuid]

    def now(self) -> datetime:
        return datetime.now(timezone.utc)


store = InMemoryStore()


class AsyncInMemoryStore:
    """Async adapter for InMemoryStore (tests / fallback)."""

    def __init__(self) -> None:
        self._store = InMemoryStore()

    def now(self) -> datetime:
        return self._store.now()

    async def upsert_player(self, record: PlayerRecord) -> None:
        self._store.upsert_player(record)

    async def upsert_match(self, record: MatchRecord) -> None:
        self._store.upsert_match(record)

    async def upsert_player_match_stats(self, record: PlayerMatchStatsRecord) -> None:
        self._store.upsert_player_match_stats(record)

    async def get_player(self, puuid: str) -> PlayerRecord | None:
        return self._store.players.get(puuid)

    async def list_player_stats(self, puuid: str) -> list[PlayerMatchStatsRecord]:
        return self._store.list_player_stats(puuid)

    def _clear_for_tests(self) -> None:
        self._store.players.clear()
        self._store.matches.clear()
        self._store.player_match_stats.clear()
