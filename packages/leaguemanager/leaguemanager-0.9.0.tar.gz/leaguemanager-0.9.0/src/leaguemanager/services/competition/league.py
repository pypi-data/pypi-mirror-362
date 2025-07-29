from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import League
from leaguemanager.repository import LeagueSyncRepository
from leaguemanager.repository._async import LeagueAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["LeagueService", "LeagueAsyncService"]


class LeagueService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = LeagueSyncRepository


class LeagueAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = LeagueAsyncRepository
