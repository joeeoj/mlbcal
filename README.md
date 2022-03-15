# mlbcal

Download the schedule for a given team using the MLB Stats API.

## installation

`pip install mlbcal`

No external dependencies to run. Need pytest to run the tests.

## usage

```
usage: mlbcal [-h] [--year YEAR] [--full] [--nopre] [--csv] team

CLI to download MLB calendar for a given team. Default output is json

positional arguments:
  team         Team name, abbreviation, or city

options:
  -h, --help   show this help message and exit
  --year YEAR  Change schedule year (default: current year)
  --full       Return unparsed response (cannot use --csv and --nopre)
  --nopre      Filter out preseason spring training games
  --csv        Format results as csv (default: json)
```

## examples

### json default

All outputs are to stdout so you need to redirect to save files. The default format is json with two space indents:

`$ mlbcal mariners > mariners.json`

### csv

`$ mlbcal yankees --csv > yankees.csv`

### flags

The default year is the current year but you can change it. I don't know how far back the MLB API will respond with data:

`$ mlbcal "San Diego" --csv --year 2021 > padres_last_year.csv`

You can also filter out preseason games with a flag:

`$ mlbcal LAA --csv --nopre > angels.csv`

You can also get the unfurled but otherwise unparsed response this way:

`$ mlbcal mets --full > mets.json`

## note on the team name lookup

`data/teams.json` contains a lookup of team ids and different variations of the team names including abbreviations and city names to allow for flexible user input for the team names. The lookup data shipped in this repo was pulled in March 2022 which means it may not align with historical team names if you lookup past schedules.

You can download the team lookup for previous seasons by providing a year argument to the `utils/download_teams.py` helper script.
