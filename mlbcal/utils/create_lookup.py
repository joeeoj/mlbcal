from collections import defaultdict
from datetime import date
import json
from pathlib import Path
from typing import List
import urllib.request


LOOKUP_FNAME = Path(__file__).cwd().parent / 'lookup' / 'teams.json'
YEAR = date.today().year
URL = f'https://statsapi.mlb.com/api/v1/teams?sportId=1&season={YEAR}'


def download_teams(url: str) -> dict:
    """Load json response from a given url"""
    with urllib.request.urlopen(url) as f:
        d = json.loads(f.read()).get('teams')
    return d


def parse_results(teams: List[dict]) -> dict:
    keys = ['abbreviation', 'teamCode', 'clubName', 'franchiseName', 'shortName']
    parsed = defaultdict(list)

    for team in teams:
        for key in keys:
            parsed[team.get('id')].append(team.get(key).lower())
    parsed[117].append('trashtros')  # bang bang

    return parsed


def save_lookup(teams: dict) -> None:
    with open(LOOKUP_FNAME, 'wt') as f:
        json.dump(teams, f, indent=2)


if __name__ == '__main__':
    teams = download_teams(URL)
    parsed = parse_results(teams)
    save_lookup(parsed)
