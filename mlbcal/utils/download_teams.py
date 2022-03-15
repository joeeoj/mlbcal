"""Helper script to recreate teams.json for a given year as an argument, otherwise defaults to current year"""
from collections import defaultdict
from datetime import date
import json
from pathlib import Path
import sys
from typing import List
import urllib.request

from mlbcal.utils.load import get_team_lookup_path


LOOKUP_FNAME = get_team_lookup_path()
YEAR = date.today().year
BASE_URL = 'https://statsapi.mlb.com/api/v1/teams?sportId=1&season={year}'


def download(url: str, year: int = YEAR) -> dict:
    """Load json response from a given url (requests.get replacement)"""
    with urllib.request.urlopen(url) as f:
        d = json.loads(f.read())
    return d


def parse_results(teams: List[dict]) -> dict:
    """Parse team results into team_id -> [names] dict"""
    keys = ['abbreviation', 'teamCode', 'clubName', 'franchiseName', 'shortName']
    parsed = defaultdict(list)

    for team in teams:
        for key in keys:
            parsed[team.get('id')].append(team.get(key).lower())
    parsed[117].append('trashtros')  # bang bang

    return parsed


if __name__ == '__main__':
    args = sys.argv

    if len(args) > 1:
        url = BASE_URL.format(year=args[1])
    else:
        url = BASE_URL.format(year=YEAR)

    teams = download(url).get('teams')
    parsed = parse_results(teams)

    with open(LOOKUP_FNAME, 'wt') as f:
        json.dump(teams, f, indent=2)
