"""The v-word resets the count — and now the count is real (CBOT-9).

State lives in data/vore.json (mounted as a volume in Docker so it survives
image updates). Every reset is appended to the history so a streak graph is
possible later. If the data dir isn't writable the cog still works, it just
forgets the streak on restart.
"""

import datetime
import json
import logging
import re

import discord
from discord import app_commands
from discord.ext import commands

from cbusbot.config import DATA_DIR, ROOT

log = logging.getLogger(__name__)

PATTERN = re.compile(r"\bvore\b")
STATE_FILE = DATA_DIR / "vore.json"
EMPTY_STATE = {"last_reset": None, "best_days": 0, "resets": []}


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class Vore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.state = self._load()

    def _load(self) -> dict:
        try:
            return json.loads(STATE_FILE.read_text())
        except FileNotFoundError:
            return dict(EMPTY_STATE)
        except (json.JSONDecodeError, OSError) as e:
            log.warning("could not read %s (%s); starting fresh", STATE_FILE, e)
            return dict(EMPTY_STATE)

    def _save(self) -> None:
        try:
            DATA_DIR.mkdir(exist_ok=True)
            tmp = STATE_FILE.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(self.state, indent=2))
            tmp.replace(STATE_FILE)
        except OSError as e:
            log.warning("could not persist vore state: %s", e)

    def _days_since_reset(self) -> int | None:
        if not self.state["last_reset"]:
            return None
        last = datetime.datetime.fromisoformat(self.state["last_reset"])
        return max((_now() - last).days, 0)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if not PATTERN.search(message.content.lower()):
            return
        days = self._days_since_reset()
        lines = [f"{message.author.mention} reset the count"]
        if days is not None:
            lines.append(f"Previous count: {days} day{'s' if days != 1 else ''}")
            if days > self.state["best_days"]:
                lines.append(
                    f"That was a new record (old best: {self.state['best_days']} days)."
                )
                self.state["best_days"] = days
        now = _now().isoformat()
        self.state["last_reset"] = now
        self.state["resets"].append(now)
        self._save()
        await message.reply("YOU RUINED IT!")
        general = self.bot.get_channel(self.bot.config.general_channel_id)
        if general is None:
            general = await self.bot.fetch_channel(self.bot.config.general_channel_id)
        await general.send("\n".join(lines), file=discord.File(ROOT / "vore.png"))

    @app_commands.command(name="vorecount", description="Days since the last v-word incident")
    async def vorecount(self, interaction: discord.Interaction) -> None:
        days = self._days_since_reset()
        if days is None:
            await interaction.response.send_message(
                "No incidents on record. The count is pristine."
            )
            return
        await interaction.response.send_message(
            f"Current count: {days} day{'s' if days != 1 else ''} without the v-word. "
            f"Best: {self.state['best_days']} days. "
            f"Total incidents on record: {len(self.state['resets'])}."
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Vore(bot))
