from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Officiating
from leaguemanager.repository import OfficiatingSyncRepository
from leaguemanager.repository._async import OfficiatingAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["OfficiatingService", "OfficiatingAsyncService"]


class OfficiatingService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = OfficiatingSyncRepository


class OfficiatingAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = OfficiatingAsyncRepository
