import pytest
from sqlalchemy import delete

from leaguemanager import models as m
from leaguemanager import services as s
from leaguemanager.core.toolbox import clear_table

org_data = {
    "name": "Test Organization",
}

league_data = {
    "name": "Test League",
}


season_data = {
    "name": "Season Test",
    "description": "Burndt",
    "projected_start_date": "2022-01-01",
}


team_data = [
    {"name": "Loro"},
    {"name": "June"},
    {"name": "Tripoli"},
    {"name": "Tres", "active": False},
]

athletes_data = [
    {"first_name": "Rob", "last_name": "Crow", "label": "Ace", "team": "Loro"},
    {"first_name": "Armistead", "last_name": "Smith IV", "label": "Bingo", "team": "Loro"},
    {"first_name": "Chris", "last_name": "Prescott", "label": "Rembrandt", "team": "Loro"},
]


@pytest.fixture(scope="module")
def org(org_service, session):
    clear_table(session, m.Organization)
    clear_table(session, m.League)
    clear_table(session, m.Season)
    clear_table(session, m.Team)
    clear_table(session, m.Ruleset)
    return org_service.create(
        {
            "name": "Test Organization for Services",
        },
        auto_commit=True,
    )


@pytest.fixture(scope="module")
def league():
    return m.League(**league_data)


@pytest.fixture(scope="module")
def properties(league_properties_service):
    return league_properties_service.create(
        {"sport": "Basketweaving", "category": "MEN", "division": "A"},
        auto_commit=True,
    )


@pytest.fixture(scope="module")
def ruleset(ruleset_service):
    return ruleset_service.create(
        {
            "number_of_games": 10,
            "sun_fixtures": True,
        },
        auto_commit=True,
    )


@pytest.fixture(scope="module")
def season():
    return m.Season(**season_data)


@pytest.fixture(scope="module")
def teams():
    return [m.Team(**data) for data in team_data]


def test_season_with_teams_active(
    session, season_service, league_service, team_member_service, team_service, org, league, season, teams
) -> None:
    league.organization_id = org.id
    new_league = league_service.create(league, auto_commit=True)
    season.league_id = new_league.id
    new_season = season_service.create(season, auto_commit=True)

    for team in teams:
        _team_memb = team_member_service.create(
            {"label": f"{team.name} member", "season_id": new_season.id}, auto_commit=True
        )
        team.team_membership_id = _team_memb.id
        _ = team_service.create(team, auto_commit=True)

    teams_in_season = season_service.all_teams(new_season.id)
    assert new_season.name == "Season Test"
    assert len(new_season.team_memberships) == len(teams)
    assert len(teams_in_season) == 3

    clear_table(session, m.League)
    clear_table(session, m.Season)
    clear_table(session, m.Team)
    clear_table(session, m.TeamMembership)


def test_season_with_teams_incl_inactive(
    session, season_service, league_service, team_member_service, team_service, org, league, season, teams
) -> None:
    league.organization_id = org.id
    new_league = league_service.create(league, auto_commit=True)
    season.league_id = new_league.id
    new_season = season_service.create(season, auto_commit=True)

    for team in teams:
        _team_memb = team_member_service.create(
            {"label": f"{team.name} member", "season_id": new_season.id}, auto_commit=True
        )
        team.team_membership_id = _team_memb.id
        _ = team_service.create(team, auto_commit=True)

    teams_in_season = season_service.all_teams(new_season.id, active=False)
    assert new_season.name == "Season Test"
    assert len(new_season.team_memberships) == len(teams)
    assert len(teams_in_season) == 4

    clear_table(session, m.League)
    clear_table(session, m.Season)
    clear_table(session, m.Team)
    clear_table(session, m.TeamMembership)


def test_season_all_athletes(
    session,
    season_service,
    league_service,
    team_member_service,
    team_service,
    athlete_service,
    individual_membership_service,
    org,
    league,
    season,
    teams,
) -> None:
    league.organization_id = org.id
    new_league = league_service.create(league, auto_commit=True)
    season.league_id = new_league.id
    new_season = season_service.create(season, auto_commit=True)

    athlete_service.create_many(athletes_data, auto_commit=True)

    rob = athlete_service.get_one_or_none(label="Ace")
    armistead = athlete_service.get_one_or_none(label="Bingo")
    chris = athlete_service.get_one_or_none(label="Rembrandt")

    for team in teams:
        _team_memb = team_member_service.create(
            {"label": f"{team.name} member", "season_id": new_season.id}, auto_commit=True
        )
        team.team_membership_id = _team_memb.id
        _ = team_service.create(team, auto_commit=True)

    loro_team = team_service.get_one_or_none(name="Loro")
    tres_team = team_service.get_one_or_none(name="Tres")

    individual_membership_service.create_many(
        [
            {"athlete_id": rob.id, "team_id": loro_team.id},
            {"athlete_id": armistead.id, "team_id": loro_team.id},
            {"athlete_id": chris.id, "team_id": tres_team.id},
        ],
        auto_commit=True,
    )

    athletes = season_service.all_athletes(new_season.id)

    assert new_season.name == "Season Test"
    assert len(new_season.team_memberships) == len(teams)
    assert len(teams) == 4
    assert len(athletes) == 2

    clear_table(session, m.League)
    clear_table(session, m.Season)
    clear_table(session, m.Team)
    clear_table(session, m.TeamMembership)
    clear_table(session, m.Athlete)
    clear_table(session, m.IndividualMembership)


def test_season_all_athletes_incl_inactive_team(
    session,
    season_service,
    league_service,
    team_member_service,
    team_service,
    athlete_service,
    individual_membership_service,
    org,
    league,
    season,
    teams,
) -> None:
    """Test that all athletes are returned, including those on inactive teams."""
    league.organization_id = org.id
    new_league = league_service.create(league, auto_commit=True)
    season.league_id = new_league.id
    new_season = season_service.create(season, auto_commit=True)

    athlete_service.create_many(athletes_data, auto_commit=True)

    rob = athlete_service.get_one_or_none(label="Ace")
    armistead = athlete_service.get_one_or_none(label="Bingo")
    chris = athlete_service.get_one_or_none(label="Rembrandt")

    for team in teams:
        _team_memb = team_member_service.create(
            {"label": f"{team.name} member", "season_id": new_season.id}, auto_commit=True
        )
        team.team_membership_id = _team_memb.id
        _ = team_service.create(team, auto_commit=True)

    loro_team = team_service.get_one_or_none(name="Loro")
    tres_team = team_service.get_one_or_none(name="Tres")

    individual_membership_service.create_many(
        [
            {"athlete_id": rob.id, "team_id": loro_team.id},
            {"athlete_id": armistead.id, "team_id": loro_team.id},
            {"athlete_id": chris.id, "team_id": tres_team.id},
        ],
        auto_commit=True,
    )

    athletes = season_service.all_athletes(new_season.id, incl_inactive_team=True)

    assert new_season.name == "Season Test"
    assert len(new_season.team_memberships) == len(teams)
    assert len(teams) == 4
    assert len(athletes) == 3

    clear_table(session, m.League)
    clear_table(session, m.Season)
    clear_table(session, m.Team)
    clear_table(session, m.TeamMembership)
    clear_table(session, m.Athlete)
    clear_table(session, m.IndividualMembership)
