"""Initial schema: players, matches, player_match_stats.

Revision ID: 001
Revises:
Create Date: 2025-03-22

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("puuid", sa.Text(), nullable=False),
        sa.Column("game_name", sa.String(255), nullable=False),
        sa.Column("tag_line", sa.String(32), nullable=False),
        sa.Column("summoner_name", sa.String(255), nullable=False),
        sa.Column("region", sa.String(8), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_players_puuid", "players", ["puuid"], unique=True)

    op.create_table(
        "matches",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("match_id", sa.Text(), nullable=False),
        sa.Column("queue", sa.String(64), nullable=False),
        sa.Column("game_duration_minutes", sa.Float(), nullable=False),
        sa.Column("played_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_matches_match_id", "matches", ["match_id"], unique=True)

    op.create_table(
        "player_match_stats",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("puuid", sa.Text(), sa.ForeignKey("players.puuid", ondelete="CASCADE"), nullable=False),
        sa.Column("match_id", sa.Text(), sa.ForeignKey("matches.match_id", ondelete="CASCADE"), nullable=False),
        sa.Column("win", sa.Boolean(), nullable=False),
        sa.Column("kills", sa.Integer(), nullable=False),
        sa.Column("deaths", sa.Integer(), nullable=False),
        sa.Column("assists", sa.Integer(), nullable=False),
        sa.Column("cs", sa.Integer(), nullable=False),
        sa.Column("vision_score", sa.Integer(), nullable=False),
        sa.Column("game_duration_minutes", sa.Float(), nullable=False),
    )
    op.create_index("ix_player_match_stats_puuid", "player_match_stats", ["puuid"])
    op.create_unique_constraint(
        "uq_player_match_stats_puuid_match", "player_match_stats", ["puuid", "match_id"]
    )


def downgrade() -> None:
    op.drop_table("player_match_stats")
    op.drop_table("matches")
    op.drop_table("players")
