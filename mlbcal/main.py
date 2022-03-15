#!/usr/bin/env python3
"""Get the schedule for a given MLB team.

Usage:

# json of the current year
$ mlbcal mariners > mariners.json

# csv without spring training
$ mlbcal BOS --csv --nopre > redsox.csv

# csv of 2021
$ mlbcal LAA --csv --year 2021 > angels.csv
"""
import argparse
import csv
import datetime
import json
from typing import List
import sys

from mlbcal.utils.download_teams import download
from mlbcal.utils.load import get_team_lookup_dict


YEAR = datetime.date.today().year
BASE_URL = ('https://statsapi.mlb.com/api/v1/schedule?'
            'sportId=1&teamId={team_id}&startDate=01/01/{year}&endDate=12/31/{year}')
TEAMS = get_team_lookup_dict()
GAME_TYPES = {
    'S': 'Spring training',
    'R': 'Regular season',
    'F': 'Wild Card',
    'D': 'Division Series',
    'L': 'League Championship Series',
    'W': 'World Series',
}


def create_url(team_id: str, year: int) -> str:
    """Create MLB Stat API url for the schedule"""
    return BASE_URL.format(team_id=team_id, year=year)


def lookup_team_id(team: str) -> int:
    """Case insensitive lookup of team id from the pre-saved lookup file"""
    # return as soon as a match is found
    for team_id, names in TEAMS.items():
        if team.lower() in names:
            return int(team_id)
    else:
        raise ValueError(f'Unable to find team name "{team}". Please try the three letter team abbreviation.')


def parse_datetime(date_str: str) -> datetime.datetime:
    """Parse ISO datetime str into a UTC datetime object"""
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)


def parse_games(unparsed_games: List[dict], lookup_team_id: int) -> List[dict]:
    """Parse the original MLB response into a list of game dicts with some added data"""
    games = []
    reg_season_game_number = 0  # assumes the MLB response is already ordered (seems to be that way)

    for g in unparsed_games:
        game_date = parse_datetime(g.get('gameDate'))
        game_date_local = game_date.astimezone()  # defaults to system tz

        status = g.get('status')
        detailed, reason = status.get('detailedState'), status.get('reason')
        final_game_status = f'{detailed} - {reason}' if reason else detailed

        teams = g.get('teams')
        game_type = g.get('gameType')

        if game_type == 'R':
            reg_season_game_number += 1

        games.append({
            # game info
            'game_id': g.get('gamePk'),  # helpful if you need to match up with the full dataset
            'reg_season_game_number': reg_season_game_number if game_type == 'R' else None,
            'season': g.get('season'),
            'game_date_iso': game_date.isoformat(),
            'game_date_local': game_date_local.strftime('%Y-%m-%d'),
            'game_day_of_week_local': game_date_local.strftime('%a'),
            'game_time_local': game_date_local.strftime('%I:%M %p'),
            'day_night': g.get('dayNight'),
            'game_type': GAME_TYPES.get(game_type, game_type),  # fall back to initial
            'desc': g.get('description', '').strip(),
            'venue': g.get('venue').get('name'),
            'venue_id': g.get('venue').get('id'),
            'scheduled_innings': g.get('scheduledInnings'),
            'series_game_number': g.get('seriesGameNumber'),
            'games_in_series': g.get('gamesInSeries'),
            'double_header': g.get('doubleHeader') == 'Y',
            'final_game_status': final_game_status,
            'home_game': lookup_team_id == teams.get('home').get('team').get('id'),

            # home
            'home_team_id': teams.get('home').get('team').get('id'),
            'home_team_name': teams.get('home').get('team').get('name'),
            'home_team_score': teams.get('home').get('score'),
            'home_team_winner': teams.get('home').get('isWinner'),
            'home_team_record_wins': teams.get('home').get('leagueRecord').get('wins'),
            'home_team_record_losses': teams.get('home').get('leagueRecord').get('losses'),
            'home_team_record_pct': teams.get('home').get('leagueRecord').get('pct'),

            # away
            'away_team_id': teams.get('away').get('team').get('id'),
            'away_team_name': teams.get('away').get('team').get('name'),
            'away_team_score': teams.get('away').get('score'),
            'away_team_winner': teams.get('away').get('isWinner'),
            'away_team_record_wins': teams.get('away').get('leagueRecord').get('wins'),
            'away_team_record_losses': teams.get('away').get('leagueRecord').get('losses'),
            'away_team_record_pct': teams.get('away').get('leagueRecord').get('pct'),
        })
    return games


def main():
    desc = 'CLI to download MLB calendar for a given team. Default output is json'
    parser = argparse.ArgumentParser(prog='mlbcal', description=desc)

    parser.add_argument('team', help='Team name, abbreviation, or city')
    parser.add_argument('--year', help='Change schedule year (default: current year)', default=YEAR)
    parser.add_argument('--full', help='Return unparsed response (cannot use --csv and --nopre)', action='store_true')
    parser.add_argument('--nopre', help='Filter out preseason spring training games', action='store_true')
    parser.add_argument('--csv', help='Format results as csv (default: json)', action='store_true')
    args = parser.parse_args()

    team_id = lookup_team_id(args.team.lower())
    url = create_url(team_id=team_id, year=args.year)
    r = download(url)
    unparsed_games = [g for d in r.get('dates') for g in d.get('games')]

    if args.full:
        sys.stdout.write(json.dumps(unparsed_games, indent=2))
        sys.exit()
    else:
        games = parse_games(unparsed_games, team_id)

    if args.nopre:
        games = [g for g in games if g['game_type'] != 'Spring training']

    if args.csv:
        header = games[0].keys()
        csvwriter = csv.writer(sys.stdout)
        csvwriter.writerow(header)
        for game in games:
            csvwriter.writerow(game.values())
    else:
        sys.stdout.write(json.dumps(games, indent=2))


if __name__ == '__main__':
    main()
