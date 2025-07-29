from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Organization
from leaguemanager.repository import OrganizationSyncRepository
from leaguemanager.repository._async import OrganizationAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["OrganizationService", "OrganizationAsyncService"]


class OrganizationService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = OrganizationSyncRepository


class OrganizationAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = OrganizationAsyncRepository
