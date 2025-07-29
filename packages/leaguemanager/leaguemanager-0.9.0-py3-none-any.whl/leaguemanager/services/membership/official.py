from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Official
from leaguemanager.repository import OfficialSyncRepository
from leaguemanager.repository._async import OfficialAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["OfficialService", "OfficialAsyncService"]


class OfficialService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = OfficialSyncRepository


class OfficialAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = OfficialAsyncRepository
