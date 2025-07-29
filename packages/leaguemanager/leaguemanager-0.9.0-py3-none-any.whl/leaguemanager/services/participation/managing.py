from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Managing
from leaguemanager.repository import ManagingSyncRepository
from leaguemanager.repository._async import ManagingAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["ManagingService", "ManagingAsyncService"]


class ManagingService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = ManagingSyncRepository


class ManagingAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = ManagingAsyncRepository
