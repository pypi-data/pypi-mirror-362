from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import LeagueProperties
from leaguemanager.repository import LeaguePropertiesSyncRepository
from leaguemanager.repository._async import LeaguePropertiesAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["LeaguePropertiesService", "LeaguePropertiesAsyncService"]


class LeaguePropertiesService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = LeaguePropertiesSyncRepository


class LeaguePropertiesAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = LeaguePropertiesAsyncRepository
