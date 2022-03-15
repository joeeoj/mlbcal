import datetime

import pytest

from mlbcal.utils.load import get_team_lookup_dict


TOTAL_MLB_TEAMS = 30
TEAMS = get_team_lookup_dict()


def test_lookup_total_teams():
    assert len(TEAMS) == TOTAL_MLB_TEAMS


def test_known_team_in_lookup_file():
    mariners = TEAMS.get('136')

    assert 'sea' in mariners
    assert 'seattle' in mariners
    assert 'mariners' in mariners
