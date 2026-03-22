"""SQLAlchemy models for DraftVision V1."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, Integer, String, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puuid: Mapped[str] = mapped_column(Text, unique=True, index=True, nullable=False)
    game_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tag_line: Mapped[str] = mapped_column(String(32), nullable=False)
    summoner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    region: Mapped[str] = mapped_column(String(8), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    match_stats: Mapped[list["PlayerMatchStats"]] = relationship(
        "PlayerMatchStats", back_populates="player", cascade="all, delete-orphan"
    )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    match_id: Mapped[str] = mapped_column(Text, unique=True, index=True, nullable=False)
    queue: Mapped[str] = mapped_column(String(64), nullable=False)
    game_duration_minutes: Mapped[float] = mapped_column(Float, nullable=False)
    played_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    player_stats: Mapped[list["PlayerMatchStats"]] = relationship(
        "PlayerMatchStats", back_populates="match", cascade="all, delete-orphan"
    )


class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    puuid: Mapped[str] = mapped_column(Text, ForeignKey("players.puuid", ondelete="CASCADE"), nullable=False)
    match_id: Mapped[str] = mapped_column(Text, ForeignKey("matches.match_id", ondelete="CASCADE"), nullable=False)
    win: Mapped[bool] = mapped_column(Boolean, nullable=False)
    kills: Mapped[int] = mapped_column(Integer, nullable=False)
    deaths: Mapped[int] = mapped_column(Integer, nullable=False)
    assists: Mapped[int] = mapped_column(Integer, nullable=False)
    cs: Mapped[int] = mapped_column(Integer, nullable=False)
    vision_score: Mapped[int] = mapped_column(Integer, nullable=False)
    game_duration_minutes: Mapped[float] = mapped_column(Float, nullable=False)

    player: Mapped["Player"] = relationship("Player", back_populates="match_stats")
    match: Mapped["Match"] = relationship("Match", back_populates="player_stats")

    __table_args__ = (
        UniqueConstraint("puuid", "match_id", name="uq_player_match_stats_puuid_match"),
    )
