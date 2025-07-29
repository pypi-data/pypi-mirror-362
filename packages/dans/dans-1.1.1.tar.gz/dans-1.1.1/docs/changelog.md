# `v1.1.0`

# v1.1.0

**2025-07-02**

## Added

- New `playbyplay` subpackage, containing its own `pbpplayerlogs` and `pbpplayerstats` endpoints (view [data_formats.md](https://github.com/oscarg617/dans/blob/main/docs/data_formats.md#playbyplay-subpackage-approach) for details)
- Caching for `playbyplay` subpackage

## Changed

- Improved `request`'s abstraction and scalability
- Homogenized the endpoints and methods of the `boxscore` and `playbyplay` subpackages

## Fixed

- Fixed test cases that make requests to `stats.nba.com` with cached responses

---

# `v1.0.4`

# v1.0.4

**2025-06-18**

## Added

- 2024-25 team data
- Test cases for missing pace values
- `SEASON_TYPE` column to `PlayerLogs`: "Regular Season" or "Playoffs"
- New adjusted DRTG metric that accounts for teams playing in weaker conferences

## Changed

- Changed dataflow: DataFrame returned from `PlayerLogs` should be inputted into `PlayerStats`

## Fixed

- Ensured that `drtg_range` list is inclusive-exclusive
- Removed system exit calls so that errors are now printed and return empty DataFrames
- Fixed incorrect calculation of average DRTG in `PlayerStats`

## Improved

- Pace-scraping efficiency: instead of going through game by game to find pace, use `Basketball-Reference` team game logs to find pace for an entire season

## Removed

- Gamescore from `PlayerLogs`

# v1.0.3

**2025-04-11**

## Fixed

- Fixed dependency bug
- Changed derivation of season column of `PlayerLogs` to account for season type

# v1.0.2

**2025-04-11**

## Fixed

- Ensured `PlayerLogs` returns all logs from the season, rather than logs from the new calendar year

---

# `v1.0.1`

# Initial Release

**2025-03-27**

`Three Endpoints`

- `PlayerStats`
- `PlayerLogs`
- `Teams`