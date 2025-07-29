from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Athlete
from leaguemanager.repository import AthleteSyncRepository
from leaguemanager.repository._async import AthleteAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["AthleteService", "AthleteAsyncService"]


class AthleteService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = AthleteSyncRepository


class AthleteAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = AthleteAsyncRepository
