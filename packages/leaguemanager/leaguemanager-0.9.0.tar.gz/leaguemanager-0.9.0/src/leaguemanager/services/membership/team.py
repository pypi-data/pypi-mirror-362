from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Team
from leaguemanager.repository import TeamSyncRepository
from leaguemanager.repository._async import TeamAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["TeamService", "TeamAsyncService"]


class TeamService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = TeamSyncRepository


class TeamAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = TeamAsyncRepository
