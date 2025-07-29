from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Site
from leaguemanager.repository import SiteSyncRepository
from leaguemanager.repository._async import SiteAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["SiteService", "SiteAsyncService"]


class SiteService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = SiteSyncRepository


class SiteAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = SiteAsyncRepository
