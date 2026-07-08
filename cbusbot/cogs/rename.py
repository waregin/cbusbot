"""Scheduled server renames (e.g. "Columbugs" on May 1).

Checks the [[renames]] table in config.toml once a day at midnight in the
configured [schedule] timezone; add entries there for monthly themes.
"""

import datetime
import logging

from discord.ext import commands, tasks

log = logging.getLogger(__name__)

# Placeholder; replaced with the configured zone in __init__ before start.
_PLACEHOLDER = datetime.time(hour=0, tzinfo=datetime.timezone.utc)


class Rename(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_rename.change_interval(time=datetime.time(hour=0, tzinfo=bot.config.tz))
        self.check_rename.start()

    async def cog_unload(self) -> None:
        self.check_rename.cancel()

    @tasks.loop(time=_PLACEHOLDER)
    async def check_rename(self) -> None:
        today = datetime.datetime.now(self.bot.config.tz)
        for entry in self.bot.config.renames:
            if (entry.month, entry.day) == (today.month, today.day):
                guild = self.bot.get_guild(self.bot.config.guild_id)
                await guild.edit(name=entry.name)
                log.info("Renamed server to %s", entry.name)

    @check_rename.before_loop
    async def before_check(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Rename(bot))
