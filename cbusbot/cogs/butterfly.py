"""Monday 10 PM: report lvl-15 members without butterfly-sanctuary access.

Builds the list locally per run (the JS version accumulated names in a
module-level global from async callbacks, so reports could race)."""

import datetime
import logging

from discord.ext import commands, tasks

log = logging.getLogger(__name__)

MONDAY = 0
AT_10PM = datetime.time(hour=22, tzinfo=datetime.datetime.now().astimezone().tzinfo)
HEADER = "The following members are level 15 but do not have access to the butterfly sanctuary:\n"


class Butterfly(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.report.start()

    async def cog_unload(self) -> None:
        self.report.cancel()

    @tasks.loop(time=AT_10PM)
    async def report(self) -> None:
        if datetime.date.today().weekday() != MONDAY:
            return
        cfg = self.bot.config
        guild = self.bot.get_guild(cfg.guild_id)
        social_roles = {cfg.caterpillar_role_id, cfg.butterfly_role_id}
        names = []
        async for member in guild.fetch_members(limit=None):
            role_ids = {r.id for r in member.roles}
            if cfg.lvl15_role_id in role_ids and not (role_ids & social_roles):
                names.append(member.display_name)
        message = HEADER + "\n".join(names)
        if len(message) > 1990:  # Discord's 2000-char message limit
            message = message[:1990] + "\n..."
        channel = self.bot.get_channel(cfg.admin_channel_id)
        if channel is None:
            channel = await self.bot.fetch_channel(cfg.admin_channel_id)
        await channel.send(message)

    @report.before_loop
    async def before_report(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Butterfly(bot))
