from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import Ruleset
from leaguemanager.repository import RulesetSyncRepository
from leaguemanager.repository._async import RulesetAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["RulesetService", "RulesetAsyncService"]


class RulesetService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = RulesetSyncRepository


class RulesetAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = RulesetAsyncRepository
