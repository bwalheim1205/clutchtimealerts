from clutchtimealerts.notifications.base import Notification
import requests
import os


class DiscordBotNotification(Notification):
    def __init__(self, bot_token: str = None, channel: int = None):
        if bot_token is None:
            bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if channel is None:
            channel = os.getenv("DISCORD_CHANNEL")
        self.bot_token = bot_token
        self.channel = channel

    def _get_channel_ids(self):
        # Fetch servers bot is in
        url = "https://discord.com/api/v10/users/@me/guilds"
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200 and r.status_code != 201:
            raise Exception(
                f"Failed to send message : (Code: {r.status_code}) {r.text}"
            )

        # Iterate through servers
        channel_ids = []
        for guild in r.json():
            r = requests.get(
                f"https://discord.com/api/v10/guilds/{guild['id']}/channels",
                headers=headers,
            )
            if r.status_code == 200:
                for channel in r.json():
                    if channel["name"] == self.channel and channel["type"] == 0:
                        channel_ids.append(channel["id"])
                        continue

        return channel_ids

    def alert_channel(self, message: str, channel_id: int = None):
        """
        Sends a message to a Discord channel using a bot token.

        Parameters:
            message (str): The message to send.
        """
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {self.bot_token}",
            "Content-Type": "application/json",
        }
        payload = {"content": message}

        # Sends the message
        requests.post(url, headers=headers, json=payload)

    def send(self, message: str):
        channel_ids = self._get_channel_ids()
        for channel_id in channel_ids:
            self.alert_channel(message, channel_id)


if __name__ == "__main__":
    # Send example message
    bot_messenger = DiscordBotNotification()
    bot_messenger.send("test message")
