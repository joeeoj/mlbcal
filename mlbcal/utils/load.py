from importlib.resources import files
from pathlib import PosixPath
import json


def get_team_lookup_path() -> PosixPath:
    """Return path to teams.json"""
    return files('mlbcal.data').joinpath('teams.json')


def get_team_lookup_dict() -> dict:
    """Load teams.json as dict"""
    source = get_team_lookup_path()
    with open(source) as f:
        teams = json.load(f)

    return teams
