from fastapi.testclient import TestClient

from api.core.storage import store
from main import app

client = TestClient(app)


def setup_function() -> None:
    store.players.clear()
    store.matches.clear()
    store.player_match_stats.clear()


def test_sync_player_and_profile_flow() -> None:
    sync_response = client.post(
        "/players/sync",
        json={"game_name": "Faker", "tag_line": "KR1", "region": "br1"},
    )
    assert sync_response.status_code == 200
    sync_data = sync_response.json()
    assert sync_data["status"] == "ok"
    assert sync_data["matches_synced"] == 20

    profile_response = client.get(f"/players/{sync_data['puuid']}/profile")
    assert profile_response.status_code == 200
    profile = profile_response.json()

    assert profile["player"]["puuid"] == sync_data["puuid"]
    assert profile["metrics"]["matches"] == 20
    assert 0 <= profile["metrics"]["winrate"] <= 100
    assert profile["metrics"]["avg_kda"] >= 0
    assert profile["metrics"]["avg_cs_per_min"] >= 0
    assert profile["metrics"]["avg_vision_score"] >= 0


def test_profile_not_found() -> None:
    response = client.get("/players/notfound/profile")
    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"


def test_sync_is_idempotent_for_same_player_matches() -> None:
    first = client.post(
        "/players/sync",
        json={"game_name": "Caps", "tag_line": "EUW", "region": "br1"},
    )
    second = client.post(
        "/players/sync",
        json={"game_name": "Caps", "tag_line": "EUW", "region": "br1"},
    )

    assert first.status_code == 200
    assert second.status_code == 200

    puuid = first.json()["puuid"]
    assert puuid == second.json()["puuid"]
    assert len(store.list_player_stats(puuid)) == 20
