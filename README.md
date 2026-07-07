# cbusbot

CbusBot is being rewritten in Python using [discord.py](https://discordpy.readthedocs.io/) 2.x.
The legacy Node.js bot (`main.js`) is kept in the repo for reference while features are ported;
see the GitHub issues for the porting backlog.

## Python bot

### Setup

```bash
python3 -m venv .venv          # requires Python 3.11+
.venv/bin/pip install -e .

cp .env.example .env           # then fill in DISCORD_TOKEN (and TENORKEY)
```

Secrets live only in `.env` (never committed). Server/channel/user IDs and the
list of enabled cogs live in `config.toml`.

### Run

```bash
.venv/bin/python -m cbusbot
```

On startup the bot loads every cog listed under `[cogs] enabled` in `config.toml`
and syncs its slash commands to the home guild. Try `/ping` in Discord (or send a
plain `ping` message) to confirm it's alive.

### Adding a feature

1. Create `cbusbot/cogs/<name>.py` with a `Cog` subclass and an `async def setup(bot)`.
2. Add `"<name>"` to `enabled` in `config.toml`.

---

## Legacy Node.js bot (reference)

```
npm install
cat main.js secretFeature.js > bot.js
pm2 start bot.js      # pm2 logs to see logs
```

The old bot expects the same `.env` file (DISCORD_TOKEN, TENORKEY) and Node 12+.
