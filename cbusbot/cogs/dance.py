"""Twerking gif when allowed users/roles say "dance".

Fires only when someone actually types the word (CBOT-1): gif-picker
messages are just a URL whose slug carries the search terms (e.g.
tenor.com/view/twerk-dance-gif-...), which is how the JS bot ended up
replying to gifs. URLs are stripped before matching, and embeds are
never inspected.
"""

import logging
import re

import discord
from discord.ext import commands

from cbusbot.gifs import GifSearchError, search_gif

log = logging.getLogger(__name__)

PATTERN = re.compile(r"\bdance\b")
URL = re.compile(r"https?://\S+")


class Dance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _allowed(self, member: discord.Member | None) -> bool:
        if member is None:
            return False
        cfg = self.bot.config
        if member.id in (cfg.elle_id, cfg.owner_id):
            return True
        role_ids = {r.id for r in getattr(member, "roles", [])}
        return bool(role_ids & {cfg.admin_role_id, cfg.birthday_role_id})

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not self._allowed(message.author):
            return
        if not PATTERN.search(URL.sub("", message.content.lower())):
            return
        try:
            await message.channel.send(await search_gif("twerking"))
        except GifSearchError as e:
            log.warning("gif search failed: %s", e)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dance(bot))
