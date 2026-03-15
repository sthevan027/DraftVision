from api.analytics.metrics import calculate_profile_metrics
from api.core.storage import PlayerMatchStatsRecord


def test_calculate_profile_metrics() -> None:
    stats = [
        PlayerMatchStatsRecord(
            puuid="p1",
            match_id="m1",
            win=True,
            kills=10,
            deaths=2,
            assists=6,
            cs=210,
            vision_score=30,
            game_duration_minutes=30,
        ),
        PlayerMatchStatsRecord(
            puuid="p1",
            match_id="m2",
            win=False,
            kills=4,
            deaths=4,
            assists=8,
            cs=180,
            vision_score=24,
            game_duration_minutes=30,
        ),
    ]

    result = calculate_profile_metrics(stats)

    assert result.matches == 2
    assert result.winrate == 50.0
    assert result.avg_kda == 5.5
    assert result.avg_cs_per_min == 6.5
    assert result.avg_vision_score == 27.0


def test_calculate_profile_metrics_empty() -> None:
    result = calculate_profile_metrics([])

    assert result.matches == 0
    assert result.winrate == 0.0
    assert result.avg_kda == 0.0
    assert result.avg_cs_per_min == 0.0
    assert result.avg_vision_score == 0.0
