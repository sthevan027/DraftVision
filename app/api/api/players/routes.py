"""HTTP routes for player vertical slice."""

from fastapi import APIRouter, Depends

from api.players.schemas import PlayerProfileResponse, SyncPlayerRequest, SyncPlayerResponse
from api.players.service import PlayerService
from api.core.deps import get_repository
from api.core.repository import PostgresRepository
from api.core.storage import AsyncInMemoryStore
from api.riot.client import get_riot_client

router = APIRouter(prefix="/players", tags=["players"])


def get_player_service(
    repo: PostgresRepository | AsyncInMemoryStore = Depends(get_repository),
) -> PlayerService:
    return PlayerService(riot_client=get_riot_client(), repository=repo)


@router.post("/sync", response_model=SyncPlayerResponse)
async def sync_player(
    payload: SyncPlayerRequest,
    service: PlayerService = Depends(get_player_service),
) -> SyncPlayerResponse:
    puuid, matches_synced = await service.sync_player(
        game_name=payload.game_name,
        tag_line=payload.tag_line,
        region=payload.region,
    )
    return SyncPlayerResponse(puuid=puuid, matches_synced=matches_synced, status="ok")


@router.get("/{puuid}/profile", response_model=PlayerProfileResponse)
async def get_player_profile(
    puuid: str,
    service: PlayerService = Depends(get_player_service),
) -> PlayerProfileResponse:
    profile = await service.get_profile(puuid)
    return PlayerProfileResponse(**profile)
