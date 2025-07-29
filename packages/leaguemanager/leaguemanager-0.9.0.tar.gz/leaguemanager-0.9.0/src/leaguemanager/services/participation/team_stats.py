from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import TeamStats
from leaguemanager.repository import TeamStatsSyncRepository
from leaguemanager.repository._async import TeamStatsAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["TeamStatsService", "TeamStatsAsyncService"]


class TeamStatsService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = TeamStatsSyncRepository


class TeamStatsAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = TeamStatsAsyncRepository
