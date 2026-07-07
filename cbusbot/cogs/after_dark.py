"""Hourly: members with both the lvl-10 and 18+ roles get the after-dark role."""

import logging

from discord.ext import commands, tasks

log = logging.getLogger(__name__)


class AfterDark(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check.start()

    async def cog_unload(self) -> None:
        self.check.cancel()

    @tasks.loop(hours=1)
    async def check(self) -> None:
        cfg = self.bot.config
        guild = self.bot.get_guild(cfg.guild_id)
        after_dark = guild.get_role(cfg.after_dark_role_id)
        async for member in guild.fetch_members(limit=None):
            role_ids = {r.id for r in member.roles}
            if (cfg.lvl10_role_id in role_ids and cfg.aged_role_id in role_ids
                    and cfg.after_dark_role_id not in role_ids):
                await member.add_roles(after_dark, reason="has lvl10 + 18+ roles")
                log.info("Added after-dark role to %s", member.display_name)

    @check.before_loop
    async def before_check(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AfterDark(bot))
