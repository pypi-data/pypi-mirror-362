from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import ManagerMembership
from leaguemanager.repository import ManagerMembershipSyncRepository
from leaguemanager.repository._async import ManagerMembershipAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["ManagerMembershipService", "ManagerMembershipAsyncService"]


class ManagerMembershipService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = ManagerMembershipSyncRepository


class ManagerMembershipAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = ManagerMembershipAsyncRepository
