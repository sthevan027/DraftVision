"""Application service for player sync/profile."""

from __future__ import annotations

from fastapi import HTTPException

from api.analytics.metrics import ProfileMetrics, calculate_profile_metrics
from api.core.storage import MatchRecord, PlayerMatchStatsRecord, PlayerRecord, store
from api.riot.client import RiotClient


class PlayerService:
    def __init__(self, riot_client: RiotClient) -> None:
        self.riot_client = riot_client

    def sync_player(self, game_name: str, tag_line: str, region: str) -> tuple[str, int]:
        riot_player = self.riot_client.get_player(
            game_name=game_name,
            tag_line=tag_line,
            region=region,
        )
        now = store.now()
        store.upsert_player(
            PlayerRecord(
                puuid=riot_player.puuid,
                game_name=riot_player.game_name,
                tag_line=riot_player.tag_line,
                summoner_name=riot_player.summoner_name,
                region=riot_player.region,
                updated_at=now,
            )
        )

        matches = self.riot_client.get_recent_ranked_matches(riot_player.puuid, count=20)
        for match in matches:
            store.upsert_match(
                MatchRecord(
                    match_id=match.match_id,
                    queue=match.queue,
                    game_duration_minutes=match.game_duration_minutes,
                    played_at=match.played_at,
                )
            )
            store.upsert_player_match_stats(
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

        return riot_player.puuid, len(matches)

    def get_profile(self, puuid: str) -> dict:
        player = store.players.get(puuid)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")

        stats = store.list_player_stats(puuid)
        metrics: ProfileMetrics = calculate_profile_metrics(stats)

        return {
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


player_service = PlayerService(riot_client=RiotClient())
