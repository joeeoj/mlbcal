import datetime
import json
from pathlib import Path

import pytest

from . import lookup_team_id, parse_datetime


TOTAL_MLB_TEAMS = 30
with open(Path(__file__).cwd() / 'lookup' / 'teams.json') as f:
    TEAMS = json.load(f)


def test_lookup_total_teams() -> None:
    assert len(TEAMS) == TOTAL_MLB_TEAMS


def test_known_team_in_lookup_file() -> None:
    mariners = TEAMS.get('136')

    assert 'sea' in mariners
    assert 'seattle' in mariners
    assert 'mariners' in mariners


def test_invalid_lookup_team_id() -> None:
    with pytest.raises(ValueError):
        lookup_team_id('fake team name')


def test_valid_lookup_team_id() -> None:
    lookup_team_id('dodgers') == 119


def test_parse_datetime() -> None:
    assert parse_datetime('2022-10-02T20:10:00Z') == datetime.datetime(2022, 10, 2, 20, 10, tzinfo=datetime.timezone.utc)
