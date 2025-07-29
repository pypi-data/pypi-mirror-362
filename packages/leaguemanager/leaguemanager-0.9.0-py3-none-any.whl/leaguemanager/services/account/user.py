from __future__ import annotations

from typing import Any
from uuid import UUID

from advanced_alchemy.filters import FilterTypes
from sqlalchemy import select

from leaguemanager.models import User, UserRole
from leaguemanager.repository import UserRoleSyncRepository, UserSyncRepository
from leaguemanager.repository._async import UserAsyncRepository, UserRoleAsyncRepository
from leaguemanager.services.base import SQLAlchemyAsyncRepositoryService, SQLAlchemySyncRepositoryService

__all__ = ["UserSyncService", "UserAsyncService", "UserRoleSyncService", "UserRoleAsyncService"]


class UserSyncService(SQLAlchemySyncRepositoryService):
    """Handles user database operations."""

    repository_type = UserSyncRepository


class UserRoleSyncService(SQLAlchemySyncRepositoryService):
    """Handles database operations in the user/role association."""

    repository_type = UserRoleSyncRepository


class UserAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles user database operations."""

    repository_type = UserAsyncRepository


class UserRoleAsyncService(SQLAlchemyAsyncRepositoryService):
    """Handles database operations in the user/role association."""

    repository_type = UserRoleAsyncRepository
