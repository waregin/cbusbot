# cbusbot

CbusBot is being rewritten in Python using [discord.py](https://discordpy.readthedocs.io/) 2.x.
The legacy Node.js bot (`main.js`, discord.js v14) is kept in the repo for reference while
features are ported; see the GitHub issues for the porting backlog.

## Python bot

### Setup

```bash
python3 -m venv .venv          # requires Python 3.11+
.venv/bin/pip install -e .

cp .env.example .env           # then fill in DISCORD_TOKEN (and TENORKEY)
```

Secrets live only in `.env` (never committed). Server/channel/user/role IDs and the
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

## Deployment

The bot only makes outbound connections to Discord, so it runs fine on a
LAN-only server — nothing needs to be exposed.

### Docker (recommended)

GitHub Actions builds `ghcr.io/waregin/cbusbot` on every push (`:latest` from
master). The server only needs Docker — no Python at all:

```bash
mkdir -p /opt/cbusbot && cd /opt/cbusbot
# copy docker-compose.yml here, and create .env with DISCORD_TOKEN / KLIPY_KEY
docker compose pull && docker compose up -d
docker compose logs -f          # watch it come up
```

Updating to a new build is the same `pull` + `up -d`. Rollback: point the
compose file at a previous `sha-…` tag from the GHCR package page.

### Native (systemd)

Needs Python 3.11+ (openSUSE Leap 15.x: `sudo zypper install python312` —
the default `python3` there is 3.6, which is too old):

```bash
cd /opt/cbusbot
python3.12 -m venv .venv
.venv/bin/pip install -e .
cp .env.example .env            # fill in secrets
sudo cp deploy/cbusbot.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now cbusbot
```

Updates: `git pull && sudo systemctl restart cbusbot`.

---

## Legacy Node.js bot (reference)

```
npm install
cat main.js secretFeature.js > bot.js
pm2 start bot.js      # pm2 logs to see logs
```

The old bot expects the same `.env` file (DISCORD_TOKEN, TENORKEY).
discord.js v14 requires a modern Node (16.11+).
