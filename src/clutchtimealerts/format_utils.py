mock_game = {
    "gameId": "0022400580",
    "gameCode": "20250117/TORMIL",
    "gameStatus": 2,
    "gameStatusText": "Q3 6:01",
    "period": 3,
    "gameClock": "PT06M01.00S",
    "gameTimeUTC": "2025-01-18T01:00:00Z",
    "gameEt": "2025-01-17T20:00:00-05:00",
    "regulationPeriods": 4,
    "ifNecessary": False,
    "seriesGameNumber": "",
    "gameLabel": "",
    "gameSubLabel": "",
    "seriesText": "",
    "seriesConference": "",
    "poRoundDesc": "",
    "gameSubtype": "",
    "isNeutral": False,
    "homeTeam": {
        "teamId": 1610612749,
        "teamName": "Bucks",
        "teamCity": "Milwaukee",
        "teamTricode": "MIL",
        "wins": 22,
        "losses": 17,
        "score": 90,
        "seed": None,
        "inBonus": "0",
        "timeoutsRemaining": 5,
        "periods": [
            {"period": 1, "periodType": "REGULAR", "score": 37},
            {"period": 2, "periodType": "REGULAR", "score": 35},
            {"period": 3, "periodType": "REGULAR", "score": 18},
            {"period": 4, "periodType": "REGULAR", "score": 0},
        ],
    },
    "awayTeam": {
        "teamId": 1610612761,
        "teamName": "Raptors",
        "teamCity": "Toronto",
        "teamTricode": "TOR",
        "wins": 10,
        "losses": 31,
        "score": 78,
        "seed": None,
        "inBonus": "0",
        "timeoutsRemaining": 4,
        "periods": [
            {"period": 1, "periodType": "REGULAR", "score": 22},
            {"period": 2, "periodType": "REGULAR", "score": 35},
            {"period": 3, "periodType": "REGULAR", "score": 21},
            {"period": 4, "periodType": "REGULAR", "score": 0},
        ],
    },
    "gameLeaders": {
        "homeLeaders": {
            "personId": 203081,
            "name": "Damian Lillard",
            "jerseyNum": "0",
            "position": "G",
            "teamTricode": "MIL",
            "playerSlug": "damian-lillard",
            "points": 24,
            "rebounds": 2,
            "assists": 7,
        },
        "awayLeaders": {
            "personId": 1629628,
            "name": "RJ Barrett",
            "jerseyNum": "9",
            "position": "FG",
            "teamTricode": "TOR",
            "playerSlug": "rj-barrett",
            "points": 19,
            "rebounds": 1,
            "assists": 7,
        },
    },
    "pbOdds": {"team": None, "odds": 0.0, "suspended": 0},
    "nbaComStream": "https://www.nba.com/game/TOR-vs-MIL-0022400580?watchLive=true",
}


def format_message(game: dict, fstring: str) -> str:
    return fstring.format(
        # Home Team Configs
        HOME_TEAM_TRI=game["homeTeam"]["teamTricode"],
        HOME_TEAM_CITY=game["homeTeam"]["teamCity"],
        HOME_TEAM_NAME=game["homeTeam"]["teamName"],
        HOME_TEAM_WINS=game["homeTeam"]["wins"],
        HOME_TEAM_LOSSES=game["homeTeam"]["losses"],
        # Away Team Configs
        AWAY_TEAM_TRI=game["awayTeam"]["teamTricode"],
        AWAY_TEAM_CITY=game["awayTeam"]["teamCity"],
        AWAY_TEAM_NAME=game["awayTeam"]["teamName"],
        AWAY_TEAM_WINS=game["awayTeam"]["wins"],
        AWAY_TEAM_LOSSES=game["awayTeam"]["losses"],
        # Game Info
        GAME_ID=game["gameId"],
        GAME_CLOCK=game["gameClock"],
        HOME_TEAM_SCORE=game["homeTeam"]["score"],
        AWAY_TEAM_SCORE=game["awayTeam"]["score"],
        GAME_STATUS_TEXT=game["gameStatusText"],
        OT_NUMBER=game["period"] - 4,
        # Stream Info
        NBA_COM_STREAM=game["nbaComStream"],
    )
