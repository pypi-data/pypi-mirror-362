from advanced_alchemy.repository import (
    SQLAlchemySyncRepository,
    SQLAlchemySyncSlugRepository,
)

from leaguemanager import models

__all__ = [
    "AddressSyncRepository",
    "CitySyncRepository",
    "CountrySyncRepository",
    "StateSyncRepository",
    "RoleSyncRepository",
    "UserSyncRepository",
    "UserRoleSyncRepository",
    "AthleteSyncRepository",
    "AthleteStatsSyncRepository",
    "FixtureSyncRepository",
    "IndividualMembershipSyncRepository",
    "LeagueSyncRepository",
    "LeaguePropertiesSyncRepository",
    "ManagerSyncRepository",
    "ManagerMembershipSyncRepository",
    "ManagingSyncRepository",
    "OfficialSyncRepository",
    "OfficiatingSyncRepository",
    "OrganizationSyncRepository",
    "PhaseSyncRepository",
    "RulesetSyncRepository",
    "SeasonSyncRepository",
    "SiteSyncRepository",
    "TeamSyncRepository",
    "TeamMembershipSyncRepository",
    "TeamStatsSyncRepository",
]


class AddressSyncRepository(SQLAlchemySyncRepository[models.Address]):
    """Address repository."""

    model_type = models.Address


class CitySyncRepository(SQLAlchemySyncRepository[models.City]):
    """City repository."""

    model_type = models.City


class CountrySyncRepository(SQLAlchemySyncRepository[models.Country]):
    """Country repository."""

    model_type = models.Country


class StateSyncRepository(SQLAlchemySyncRepository[models.State]):
    """State repository."""

    model_type = models.Country


class RoleSyncRepository(SQLAlchemySyncSlugRepository[models.Role]):
    """Role repository."""

    model_type = models.Role


class UserSyncRepository(SQLAlchemySyncRepository[models.User]):
    """User repository."""

    model_type = models.User


class UserRoleSyncRepository(SQLAlchemySyncRepository[models.UserRole]):
    """UserRole repository."""

    model_type = models.UserRole


class AthleteSyncRepository(SQLAlchemySyncRepository[models.Athlete]):
    """Athlete repository."""

    model_type = models.Athlete


class AthleteStatsSyncRepository(SQLAlchemySyncRepository[models.AthleteStats]):
    """AthleteStats repository."""

    model_type = models.AthleteStats


class FixtureSyncRepository(SQLAlchemySyncRepository[models.Fixture]):
    """Fixture repository."""

    model_type = models.Fixture


class IndividualMembershipSyncRepository(SQLAlchemySyncRepository[models.IndividualMembership]):
    """IndividualMembership repository."""

    model_type = models.IndividualMembership


class LeagueSyncRepository(SQLAlchemySyncSlugRepository[models.League]):
    """League repository."""

    model_type = models.League


class LeaguePropertiesSyncRepository(SQLAlchemySyncSlugRepository[models.LeagueProperties]):
    """LeagueProperties repository."""

    model_type = models.LeagueProperties


class ManagerSyncRepository(SQLAlchemySyncRepository[models.Manager]):
    """Manager repository."""

    model_type = models.Manager


class ManagerMembershipSyncRepository(SQLAlchemySyncRepository[models.ManagerMembership]):
    """ManagerMembership repository."""

    model_type = models.ManagerMembership


class ManagingSyncRepository(SQLAlchemySyncRepository[models.Managing]):
    """Managing repository."""

    model_type = models.Managing


class OfficialSyncRepository(SQLAlchemySyncRepository[models.Official]):
    """Official repository."""

    model_type = models.Official


class OfficiatingSyncRepository(SQLAlchemySyncRepository[models.Officiating]):
    """Officiating repository."""

    model_type = models.Officiating


class OrganizationSyncRepository(SQLAlchemySyncSlugRepository[models.Organization]):
    """Organization repository."""

    model_type = models.Organization


class PhaseSyncRepository(SQLAlchemySyncRepository[models.Phase]):
    """Phase repository."""

    model_type = models.Phase


class RulesetSyncRepository(SQLAlchemySyncRepository[models.Ruleset]):
    """Ruleset repository."""

    model_type = models.Ruleset


class SeasonSyncRepository(SQLAlchemySyncSlugRepository[models.Season]):
    """Season repository."""

    model_type = models.Season


class SiteSyncRepository(SQLAlchemySyncSlugRepository[models.Site]):
    """Site repository."""

    model_type = models.Site


class TeamSyncRepository(SQLAlchemySyncSlugRepository[models.Team]):
    """Team repository."""

    model_type = models.Team


class TeamMembershipSyncRepository(SQLAlchemySyncSlugRepository[models.TeamMembership]):
    """TeamMembership repository."""

    model_type = models.TeamMembership


class TeamStatsSyncRepository(SQLAlchemySyncSlugRepository[models.TeamStats]):
    """TeamStats repository."""

    model_type = models.TeamStats
