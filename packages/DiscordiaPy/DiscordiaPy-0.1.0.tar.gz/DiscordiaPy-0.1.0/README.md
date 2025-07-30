# discordiapy

**discordiapy** is a basic python wrapper for discord's rest api (bot token only).  
it lets you interact with discord as a bot without needing a gateway connection—just use http requests.

---

## features

- get bot, user, server, and channel info
- list server channels and members
- send, edit, and delete messages
- add reactions to messages

---

## installation

install from pypi:

```sh
pip install discordiapy
```

or, for development, clone the repo and install dependencies:

```sh
pip install -r requirements.txt
```

---

## usage

```python
from client import discordiapy

token = ""
client = discordiapy(token)

# get info about the bot user
print(client.get_me())

# send a message
channel_id = ""
client.send_message(channel_id, "hi from discordia")
```

---

## requirements

- python 3.7+
- `requests` library

---

## project structure
- 📂 discordiapy
- `client.py` – main api wrapper
- `__init__.py` – version and imports
-  ❌ no folder
- `pyproject.toml` – build system
- `setup.cfg` – package metadata/configuration
- `setup.py` - package metadata/configuration
- `readme.md` – this file
- `license` – license
- 📂 dist
- `discordia-0.1.0.tar.gz` - tar.gz file for installing
- `Discordia-0.1.0-py3-none-any.whl` .whl file for installing

---

## license

[mit](LICENSE)

---