from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Phase
from leaguemanager.repository import PhaseSyncRepository
from leaguemanager.repository._async import PhaseAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["PhaseService", "PhaseAsyncService"]


class PhaseService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = PhaseSyncRepository


class PhaseAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = PhaseAsyncRepository
