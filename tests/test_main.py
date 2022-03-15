import datetime

import pytest

from mlbcal.main import lookup_team_id, parse_datetime


def test_invalid_lookup_team_id():
    with pytest.raises(ValueError):
        lookup_team_id('fake team name')


def test_valid_lookup_team_id():
    lookup_team_id('dodgers') == 119


def test_lookup_team_id_data_type():
    assert type(lookup_team_id('dodgers')) is int


def test_parse_datetime():
    assert parse_datetime('2022-10-02T20:10:00Z') == datetime.datetime(2022,10,2,20,10, tzinfo=datetime.timezone.utc)
