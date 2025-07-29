from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import TeamMembership
from leaguemanager.repository import TeamMembershipSyncRepository
from leaguemanager.repository._async import TeamMembershipAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["TeamMembershipService", "TeamMembershipAsyncService"]


class TeamMembershipService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = TeamMembershipSyncRepository


class TeamMembershipAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = TeamMembershipAsyncRepository
