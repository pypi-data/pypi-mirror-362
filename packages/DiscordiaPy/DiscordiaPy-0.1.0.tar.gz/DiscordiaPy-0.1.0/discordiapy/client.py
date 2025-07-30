import requests

class DiscordAPIError(Exception):
    pass

class DiscordiaPy:
    """
    basic python wrapper for discord's rest api.
    """

    api_url = "https://discord.com/api/v10"

    def __init__(self, token: str):
        if not token:
            raise ValueError("no discord bot token provided")
        self.token = token

    def _headers(self):
        return {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordiaPy/0.1.0"
        }

    # user stuff
    def get_me(self):
        url = f"{self.api_url}/users/@me"
        resp = requests.get(url, headers=self._headers())
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't get current user: {resp.text}")
        return resp.json()

    def get_user(self, user_id: str):
        url = f"{self.api_url}/users/{user_id}"
        resp = requests.get(url, headers=self._headers())
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't get user: {resp.text}")
        return resp.json()

    # server/guild stuff
    def get_server(self, server_id: str):
        url = f"{self.api_url}/guilds/{server_id}"
        resp = requests.get(url, headers=self._headers())
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't get server: {resp.text}")
        return resp.json()

    def get_server_channels(self, server_id: str):
        url = f"{self.api_url}/guilds/{server_id}/channels"
        resp = requests.get(url, headers=self._headers())
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't get server channels: {resp.text}")
        return resp.json()

    def get_members(self, server_id: str, limit=1000):
        url = f"{self.api_url}/guilds/{server_id}/members"
        params = {"limit": limit}
        resp = requests.get(url, headers=self._headers(), params=params)
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't get members: {resp.text}")
        return resp.json()

    # channel stuff
    def get_channel(self, channel_id: str):
        url = f"{self.api_url}/channels/{channel_id}"
        resp = requests.get(url, headers=self._headers())
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't get channel: {resp.text}")
        return resp.json()

    def send_message(self, channel_id: str, text: str, tts=False, embed=None):
        url = f"{self.api_url}/channels/{channel_id}/messages"
        data = {"content": text, "tts": tts}
        if embed:
            data["embed"] = embed
        resp = requests.post(url, headers=self._headers(), json=data)
        if resp.status_code not in (200, 201):
            raise DiscordAPIError(f"couldn't send message: {resp.text}")
        return resp.json()

    def get_channel_messages(self, channel_id: str, limit=50):
        url = f"{self.api_url}/channels/{channel_id}/messages"
        params = {"limit": limit}
        resp = requests.get(url, headers=self._headers(), params=params)
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't get messages: {resp.text}")
        return resp.json()

    # reactions
    def add_reaction(self, channel_id: str, message_id: str, emoji: str):
        url = f"{self.api_url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
        resp = requests.put(url, headers=self._headers())
        if resp.status_code != 204:
            raise DiscordAPIError(f"couldn't add reaction: {resp.text}")
        return True

    # editing and deleting
    def edit_message(self, channel_id: str, message_id: str, text: str):
        url = f"{self.api_url}/channels/{channel_id}/messages/{message_id}"
        data = {"content": text}
        resp = requests.patch(url, headers=self._headers(), json=data)
        if resp.status_code != 200:
            raise DiscordAPIError(f"couldn't edit message: {resp.text}")
        return resp.json()

    def delete_message(self, channel_id: str, message_id: str):
        url = f"{self.api_url}/channels/{channel_id}/messages/{message_id}"
        resp = requests.delete(url, headers=self._headers())
        if resp.status_code != 204:
            raise DiscordAPIError(f"couldn't delete message: {resp.text}")
        return True