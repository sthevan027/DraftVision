"""Repository layer for players, matches and stats."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.models import Match, Player, PlayerMatchStats
from api.core.storage import MatchRecord, PlayerMatchStatsRecord, PlayerRecord


class PlayerRepositoryProtocol(Protocol):
    """Protocol for player/match persistence."""

    async def upsert_player(self, record: PlayerRecord) -> None: ...
    async def upsert_match(self, record: MatchRecord) -> None: ...
    async def upsert_player_match_stats(self, record: PlayerMatchStatsRecord) -> None: ...
    async def get_player(self, puuid: str) -> PlayerRecord | None: ...
    async def list_player_stats(self, puuid: str) -> list[PlayerMatchStatsRecord]: ...
    def now(self) -> datetime: ...


class PostgresRepository:
    """PostgreSQL implementation of the player repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    async def upsert_player(self, record: PlayerRecord) -> None:
        stmt = insert(Player).values(
            puuid=record.puuid,
            game_name=record.game_name,
            tag_line=record.tag_line,
            summoner_name=record.summoner_name,
            region=record.region,
            updated_at=record.updated_at,
        ).on_conflict_do_update(
            index_elements=["puuid"],
            set_=dict(
                game_name=record.game_name,
                tag_line=record.tag_line,
                summoner_name=record.summoner_name,
                region=record.region,
                updated_at=record.updated_at,
            ),
        )
        await self._session.execute(stmt)

    async def upsert_match(self, record: MatchRecord) -> None:
        stmt = insert(Match).values(
            match_id=record.match_id,
            queue=record.queue,
            game_duration_minutes=record.game_duration_minutes,
            played_at=record.played_at,
        ).on_conflict_do_nothing(index_elements=["match_id"])
        await self._session.execute(stmt)

    async def upsert_player_match_stats(self, record: PlayerMatchStatsRecord) -> None:
        stmt = insert(PlayerMatchStats).values(
            puuid=record.puuid,
            match_id=record.match_id,
            win=record.win,
            kills=record.kills,
            deaths=record.deaths,
            assists=record.assists,
            cs=record.cs,
            vision_score=record.vision_score,
            game_duration_minutes=record.game_duration_minutes,
        ).on_conflict_do_update(
            index_elements=["puuid", "match_id"],
            set_=dict(
                win=record.win,
                kills=record.kills,
                deaths=record.deaths,
                assists=record.assists,
                cs=record.cs,
                vision_score=record.vision_score,
                game_duration_minutes=record.game_duration_minutes,
            ),
        )
        await self._session.execute(stmt)

    async def get_player(self, puuid: str) -> PlayerRecord | None:
        result = await self._session.execute(select(Player).where(Player.puuid == puuid))
        row = result.scalar_one_or_none()
        if not row:
            return None
        return PlayerRecord(
            puuid=row.puuid,
            game_name=row.game_name,
            tag_line=row.tag_line,
            summoner_name=row.summoner_name,
            region=row.region,
            updated_at=row.updated_at,
        )

    async def list_player_stats(self, puuid: str) -> list[PlayerMatchStatsRecord]:
        result = await self._session.execute(
            select(PlayerMatchStats).where(PlayerMatchStats.puuid == puuid)
        )
        rows = result.scalars().all()
        return [
            PlayerMatchStatsRecord(
                puuid=r.puuid,
                match_id=r.match_id,
                win=r.win,
                kills=r.kills,
                deaths=r.deaths,
                assists=r.assists,
                cs=r.cs,
                vision_score=r.vision_score,
                game_duration_minutes=r.game_duration_minutes,
            )
            for r in rows
        ]
