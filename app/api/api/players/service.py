"""Application service for player sync/profile."""

from __future__ import annotations

from fastapi import HTTPException

from api.analytics.metrics import ProfileMetrics, calculate_profile_metrics
from api.core.cache import get_cached_profile, invalidate_profile, set_cached_profile
from api.core.repository import PostgresRepository
from api.core.storage import (
    AsyncInMemoryStore,
    MatchRecord,
    PlayerMatchStatsRecord,
    PlayerRecord,
)
from api.riot.client import RiotClientProtocol

PROFILE_CACHE_TTL = 300  # 5 minutes


class PlayerService:
    def __init__(
        self,
        riot_client: RiotClientProtocol,
        repository: PostgresRepository | AsyncInMemoryStore,
    ) -> None:
        self.riot_client = riot_client
        self.repo = repository

    async def sync_player(
        self, game_name: str, tag_line: str, region: str
    ) -> tuple[str, int]:
        riot_player = self.riot_client.get_player(
            game_name=game_name,
            tag_line=tag_line,
            region=region,
        )
        now = self.repo.now()
        await self.repo.upsert_player(
            PlayerRecord(
                puuid=riot_player.puuid,
                game_name=riot_player.game_name,
                tag_line=riot_player.tag_line,
                summoner_name=riot_player.summoner_name,
                region=riot_player.region,
                updated_at=now,
            )
        )

        matches = self.riot_client.get_recent_ranked_matches(
            riot_player.puuid, count=20, region=riot_player.region
        )
        for match in matches:
            await self.repo.upsert_match(
                MatchRecord(
                    match_id=match.match_id,
                    queue=match.queue,
                    game_duration_minutes=match.game_duration_minutes,
                    played_at=match.played_at,
                )
            )
            await self.repo.upsert_player_match_stats(
                PlayerMatchStatsRecord(
                    puuid=riot_player.puuid,
                    match_id=match.match_id,
                    win=match.win,
                    kills=match.kills,
                    deaths=match.deaths,
                    assists=match.assists,
                    cs=match.cs,
                    vision_score=match.vision_score,
                    game_duration_minutes=match.game_duration_minutes,
                )
            )

        await invalidate_profile(riot_player.puuid)
        return riot_player.puuid, len(matches)

    async def get_profile(self, puuid: str) -> dict:
        cached = await get_cached_profile(puuid)
        if cached:
            return cached

        player = await self.repo.get_player(puuid)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        stats = await self.repo.list_player_stats(puuid)
        metrics: ProfileMetrics = calculate_profile_metrics(stats)

        profile = {
            "player": {
                "puuid": player.puuid,
                "summoner_name": player.summoner_name,
                "region": player.region,
            },
            "metrics": {
                "matches": metrics.matches,
                "winrate": metrics.winrate,
                "avg_kda": metrics.avg_kda,
                "avg_cs_per_min": metrics.avg_cs_per_min,
                "avg_vision_score": metrics.avg_vision_score,
            },
            "updated_at": player.updated_at.isoformat(),
        }
        await set_cached_profile(puuid, profile, ttl_seconds=PROFILE_CACHE_TTL)
        return profile
