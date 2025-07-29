from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Fixture
from leaguemanager.repository import FixtureSyncRepository
from leaguemanager.repository._async import FixtureAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["FixtureService", "FixtureAsyncService"]


class FixtureService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = FixtureSyncRepository


class FixtureAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = FixtureAsyncRepository
