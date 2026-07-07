"""Wednesday-noon siren gif in general."""

import datetime
import logging
import random

from discord.ext import commands, tasks

from cbusbot.gifs import GifSearchError, search_gif

log = logging.getLogger(__name__)

SEARCH_WORDS = ["woooo", "siren", "awoo"]
WEDNESDAY = 2
# Server-local noon, matching the old node-cron behavior (naive times in
# tasks.loop would be treated as UTC).
NOON = datetime.time(hour=12, tzinfo=datetime.datetime.now().astimezone().tzinfo)


class Siren(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.siren.start()

    async def cog_unload(self) -> None:
        self.siren.cancel()

    @tasks.loop(time=NOON)
    async def siren(self) -> None:
        if datetime.date.today().weekday() != WEDNESDAY:
            return
        channel = self.bot.get_channel(self.bot.config.general_channel_id)
        if channel is None:
            channel = await self.bot.fetch_channel(self.bot.config.general_channel_id)
        try:
            await channel.send(await search_gif(random.choice(SEARCH_WORDS)))
        except GifSearchError as e:
            log.warning("siren gif search failed: %s", e)

    @siren.before_loop
    async def before_siren(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Siren(bot))
