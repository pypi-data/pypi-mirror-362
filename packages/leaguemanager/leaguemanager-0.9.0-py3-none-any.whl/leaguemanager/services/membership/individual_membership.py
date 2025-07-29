from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import IndividualMembership
from leaguemanager.repository import IndividualMembershipSyncRepository
from leaguemanager.repository._async import IndividualMembershipAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["IndividualMembershipService", "IndividualMembershipAsyncService"]


class IndividualMembershipService(SQLAlchemySyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = IndividualMembershipSyncRepository


class IndividualMembershipAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations for roles data."""

    repository_type = IndividualMembershipAsyncRepository
