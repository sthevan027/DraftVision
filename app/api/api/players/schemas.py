"""Pydantic schemas for player endpoints."""

from pydantic import BaseModel, Field


class SyncPlayerRequest(BaseModel):
    game_name: str = Field(min_length=1)
    tag_line: str = Field(min_length=1)
    region: str = Field(default="br1", min_length=2)


class SyncPlayerResponse(BaseModel):
    puuid: str
    matches_synced: int
    status: str


class PlayerData(BaseModel):
    puuid: str
    summoner_name: str
    region: str


class ProfileMetricsData(BaseModel):
    matches: int
    winrate: float
    avg_kda: float
    avg_cs_per_min: float
    avg_vision_score: float


class PlayerProfileResponse(BaseModel):
    player: PlayerData
    metrics: ProfileMetricsData
    updated_at: str
