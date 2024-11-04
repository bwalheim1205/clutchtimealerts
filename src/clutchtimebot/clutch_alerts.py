from clutchtimebot.scraper.live_scores import NBAScoreScraper
import time


class ClutchAlertsService:
    def __init__(self):
        self.scraper = NBAScoreScraper()

    def send_clutch_alert(self, message) -> None:
        # TODO: Send alert via configured messaging platform (e.g., Discord, Slack, SMS)
        print(message)

    def _get_minutes_from_clock(self, clock) -> int:
        """
        Extract the minutes from the given clock string.

        The clock string is expected to be in the format "PT{minutes}M{seconds}S"
        If the string is empty or not in this format, -1 is returned.

        Parameters
        ----------
        clock : str
            The clock string to extract the minutes from.

        Returns
        -------
        int
            The minutes if the string is in the correct format, otherwise -1.
        """
        try:
            return int(clock.split("PT")[1].split("M")[0])
        except Exception:
            return -1

    def isCluthTime(self, game: dict) -> bool:
        """
        Checks if the given game is in "clutch time" - the last five minutes of the fourth quarter
        or overtime with the point difference being five points or fewer.

        Parameters
        ----------
        game : dict
            The game data to check.

        Returns
        -------
        bool
            True if the game is in clutch time, otherwise False.
        """
        period = game["period"]
        homeTeamScore = game["homeTeam"]["score"]
        awayTeamScore = game["awayTeam"]["score"]
        clock = game["gameClock"]
        minutes = self._get_minutes_from_clock(clock)

        if period < 4:
            return False
        elif minutes == -1 or minutes >= 5:
            return False
        elif minutes < 5:
            return False
        elif abs(homeTeamScore - awayTeamScore) > 5:
            return False

        return True

    def run(self) -> None:
        while True:
            # Fetch live games
            games = self.scraper.live_games()

            # Iterate through each live game and send alert
            for game in games:
                if self.isCluthTime(game):
                    homeTeam = game["homeTeam"]["teamTricode"]
                    awayTeam = game["awayTeam"]["teamTricode"]
                    homeTeamScore = game["homeTeam"]["score"]
                    awayTeamScore = game["awayTeam"]["score"]
                    self.send_clutch_alert(
                        f"{homeTeam} {homeTeamScore} - {awayTeamScore} {awayTeam}"
                    )

            # Sleep for 2 hours if there are no live games
            if len(games) == 0:
                time.sleep(7200)
            # Otherwise sleep for 30 seconds
            else:
                time.sleep(30)
