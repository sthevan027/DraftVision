"""HTTP routes for player vertical slice."""

from fastapi import APIRouter

from api.players.schemas import PlayerProfileResponse, SyncPlayerRequest, SyncPlayerResponse
from api.players.service import player_service

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/sync", response_model=SyncPlayerResponse)
async def sync_player(payload: SyncPlayerRequest) -> SyncPlayerResponse:
    puuid, matches_synced = player_service.sync_player(
        game_name=payload.game_name,
        tag_line=payload.tag_line,
        region=payload.region,
    )
    return SyncPlayerResponse(puuid=puuid, matches_synced=matches_synced, status="ok")


@router.get("/{puuid}/profile", response_model=PlayerProfileResponse)
async def get_player_profile(puuid: str) -> PlayerProfileResponse:
    profile = player_service.get_profile(puuid)
    return PlayerProfileResponse(**profile)
