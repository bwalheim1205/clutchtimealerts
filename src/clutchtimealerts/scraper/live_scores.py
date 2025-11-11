import requests


class NBAScoreScraper:
    BASE_URL = "https://cdn.nba.com/static/json/liveData/"
    ENDPOINT = "scoreboard/todaysScoreboard_00.json"

    # Mimic web browser headers
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "cdn.nba.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

    def __init__(self):
        """
        Initialize the NBAScoreScraper. This sets the URL that will be used to
        load the scoreboard data from the NBA website.
        """
        self.url = self.BASE_URL + self.ENDPOINT

    def load_json(self) -> dict:
        """
        Fetch the JSON data from the NBA scoreboard API.

        Sends a GET request to the pre-defined URL and retrieves the JSON data
        if the response is successful. Returns None if the request fails.

        Returns:
            dict: Parsed JSON data from the response if successful, otherwise None.
        """
        r = requests.get(self.url)
        if r.status_code != 200:
            return None
        return r.json()

    def live_games(self) -> list[dict]:
        """
        Returns a list of live games (gameStatus == 2).

        Returns:
            list: A list of live games, with each game represented as a dict.
        """
        data = self.load_json()
        if data is None:
            return []
        live_games = [
            game for game in data["scoreboard"]["games"] if game["gameStatus"] == 2
        ]
        return live_games


if __name__ == "__main__":
    scraper = NBAScoreScraper()
    games = scraper.live_games()
    for game in games:
        homeTeam = game["homeTeam"]["teamTricode"]
        awayTeam = game["awayTeam"]["teamTricode"]
        homeTeamScore = game["homeTeam"]["score"]
        awayTeamScore = game["awayTeam"]["score"]
        print(f"{homeTeam} {homeTeamScore} - {awayTeamScore} {awayTeam}")
