from advanced_alchemy.repository import (
    SQLAlchemyAsyncRepository,
    SQLAlchemyAsyncSlugRepository,
)

from leaguemanager import models

__all__ = [
    "AddressAsyncRepository",
    "CityAsyncRepository",
    "CountryAsyncRepository",
    "StateAsyncRepository",
    "RoleAsyncRepository",
    "UserAsyncRepository",
    "UserRoleAsyncRepository",
    "AthleteAsyncRepository",
    "AthleteStatsAsyncRepository",
    "FixtureAsyncRepository",
    "IndividualMembershipAsyncRepository",
    "LeagueAsyncRepository",
    "LeaguePropertiesAsyncRepository",
    "ManagerAsyncRepository",
    "ManagerMembershipAsyncRepository",
    "ManagingAsyncRepository",
    "OfficialAsyncRepository",
    "OfficiatingAsyncRepository",
    "OrganizationAsyncRepository",
    "PhaseAsyncRepository",
    "RulesetAsyncRepository",
    "SeasonAsyncRepository",
    "SiteAsyncRepository",
    "TeamAsyncRepository",
    "TeamMembershipAsyncRepository",
    "TeamStatsAsyncRepository",
]


class AddressAsyncRepository(SQLAlchemyAsyncRepository[models.Address]):
    """Address repository."""

    model_type = models.Address


class CityAsyncRepository(SQLAlchemyAsyncRepository[models.City]):
    """City repository."""

    model_type = models.City


class CountryAsyncRepository(SQLAlchemyAsyncRepository[models.Country]):
    """Country repository."""

    model_type = models.Country


class StateAsyncRepository(SQLAlchemyAsyncRepository[models.State]):
    """State repository."""

    model_type = models.Country


class RoleAsyncRepository(SQLAlchemyAsyncSlugRepository[models.Role]):
    """Role repository."""

    model_type = models.Role


class UserAsyncRepository(SQLAlchemyAsyncRepository[models.User]):
    """User repository."""

    model_type = models.User


class UserRoleAsyncRepository(SQLAlchemyAsyncRepository[models.UserRole]):
    """UserRole repository."""

    model_type = models.UserRole


class AthleteAsyncRepository(SQLAlchemyAsyncRepository[models.Athlete]):
    """Athlete repository."""

    model_type = models.Athlete


class AthleteStatsAsyncRepository(SQLAlchemyAsyncRepository[models.AthleteStats]):
    """AthleteStats repository."""

    model_type = models.AthleteStats


class FixtureAsyncRepository(SQLAlchemyAsyncRepository[models.Fixture]):
    """Fixture repository."""

    model_type = models.Fixture


class IndividualMembershipAsyncRepository(SQLAlchemyAsyncRepository[models.IndividualMembership]):
    """IndividualMembership repository."""

    model_type = models.IndividualMembership


class LeagueAsyncRepository(SQLAlchemyAsyncSlugRepository[models.League]):
    """League repository."""

    model_type = models.League


class LeaguePropertiesAsyncRepository(SQLAlchemyAsyncSlugRepository[models.LeagueProperties]):
    """LeagueProperties repository."""

    model_type = models.LeagueProperties


class ManagerAsyncRepository(SQLAlchemyAsyncRepository[models.Manager]):
    """Manager repository."""

    model_type = models.Manager


class ManagerMembershipAsyncRepository(SQLAlchemyAsyncRepository[models.ManagerMembership]):
    """ManagerMembership repository."""

    model_type = models.ManagerMembership


class ManagingAsyncRepository(SQLAlchemyAsyncRepository[models.Managing]):
    """Managing repository."""

    model_type = models.Managing


class OfficialAsyncRepository(SQLAlchemyAsyncRepository[models.Official]):
    """Official repository."""

    model_type = models.Official


class OfficiatingAsyncRepository(SQLAlchemyAsyncRepository[models.Officiating]):
    """Officiating repository."""

    model_type = models.Officiating


class OrganizationAsyncRepository(SQLAlchemyAsyncSlugRepository[models.Organization]):
    """Organization repository."""

    model_type = models.Organization


class PhaseAsyncRepository(SQLAlchemyAsyncRepository[models.Phase]):
    """Phase repository."""

    model_type = models.Phase


class RulesetAsyncRepository(SQLAlchemyAsyncSlugRepository[models.Ruleset]):
    """Ruleset repository."""

    model_type = models.Ruleset


class SeasonAsyncRepository(SQLAlchemyAsyncSlugRepository[models.Season]):
    """Season repository."""

    model_type = models.Season


class SiteAsyncRepository(SQLAlchemyAsyncSlugRepository[models.Site]):
    """Site repository."""

    model_type = models.Site


class TeamAsyncRepository(SQLAlchemyAsyncSlugRepository[models.Team]):
    """Team repository."""

    model_type = models.Team


class TeamMembershipAsyncRepository(SQLAlchemyAsyncSlugRepository[models.TeamMembership]):
    """TeamMembership repository."""

    model_type = models.TeamMembership


class TeamStatsAsyncRepository(SQLAlchemyAsyncSlugRepository[models.TeamStats]):
    """TeamStats repository."""

    model_type = models.TeamStats
