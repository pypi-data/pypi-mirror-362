from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import AthleteStats
from leaguemanager.repository import AthleteStatsSyncRepository
from leaguemanager.repository._async import AthleteStatsAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["AthleteStatsService", "AthleteStatsAsyncService"]


class AthleteStatsService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = AthleteStatsSyncRepository


class AthleteStatsAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = AthleteStatsAsyncRepository
