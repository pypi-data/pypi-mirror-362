'''Headers and parameters used to send requests to stats.nba.com'''
def _standard_header() -> dict:
    return {"accept": "application/json, text/plain,*/*","accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9", "origin": "https://www.nba.com",
    "referer": "https://www.nba.com/","sec-fetch-dest": "empty", "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

def _player_logs_params(measure_type, per_mode, season_year, season_type):

    return (("DateFrom", ""), ("DateTo", ""), ("GameSegment", ""), ("LastNGames", ""),
            ("LeagueID", ""), ("Location", ""), ("MeasureType", measure_type), ("Month", ""),
            ("OpponentTeamID", None), ("Outcome", ""), ("PORound", ""), ("PerMode", per_mode),
            ("Period", ""), ("PlayerID", ""), ("Season", season_year), ("SeasonSegment", ""),
            ("SeasonType", season_type), ("ShotClockRange", ""), ("TeamID", ""),
            ("VsConference", ""), ("VsDivision", ""))

def _team_advanced_params(measure_type, per_mode, season_year, season_type):
    return (("Conference", ""), ("DateFrom", ""), ("DateTo", ""), ("Division", ""),
            ("GameScope", ""), ("GameSegment", ""), {"Height", ""}, ("LastNGames", "0"),
            ("LeagueID", "00"), ("Location", ""), ("MeasureType", measure_type), ("Month", "0"),
            ("OpponentTeamID", "0"), ("Outcome", ""), ("PORound", "0"), ("PaceAdjust", "N"),
            ("PerMode", per_mode), ("Period", "0"), ("PlayerExperience", ""),
            ("PlayerPosition", ""), ("PlusMinus", "N"), ("Rank", "N"), ("Season", season_year),
            ("SeasonSegment", ""), ("SeasonType", season_type), ("ShotClockRange", ""),
            ("StarterBench", ""), ("TeamID", "0"), ("TwoWay", "0"), ("VsConference", ""),
            ("VsDivision", "" ))
