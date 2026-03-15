"""Metric calculations for player profile."""

from __future__ import annotations

from dataclasses import dataclass

from api.core.storage import PlayerMatchStatsRecord


@dataclass
class ProfileMetrics:
    matches: int
    winrate: float
    avg_kda: float
    avg_cs_per_min: float
    avg_vision_score: float


def calculate_profile_metrics(stats: list[PlayerMatchStatsRecord]) -> ProfileMetrics:
    if not stats:
        return ProfileMetrics(
            matches=0,
            winrate=0.0,
            avg_kda=0.0,
            avg_cs_per_min=0.0,
            avg_vision_score=0.0,
        )

    matches = len(stats)
    wins = sum(1 for item in stats if item.win)
    total_kda = 0.0
    total_cs_per_min = 0.0
    total_vision = 0

    for item in stats:
        deaths = item.deaths if item.deaths > 0 else 1
        total_kda += (item.kills + item.assists) / deaths
        if item.game_duration_minutes > 0:
            total_cs_per_min += item.cs / item.game_duration_minutes
        total_vision += item.vision_score

    return ProfileMetrics(
        matches=matches,
        winrate=round((wins / matches) * 100, 2),
        avg_kda=round(total_kda / matches, 2),
        avg_cs_per_min=round(total_cs_per_min / matches, 2),
        avg_vision_score=round(total_vision / matches, 2),
    )
