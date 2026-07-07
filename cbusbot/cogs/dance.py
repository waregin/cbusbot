"""Twerking gif when allowed users/roles mention dancing.

Fixes CBOT-1: gif messages carry "dance" in their embed description, and
Discord attaches embeds asynchronously (often via a message edit after
delivery), so the JS bot's content-only check never saw them. We check
embeds too, and watch on_message_edit for embeds that arrive late.
"""

import logging
import re

import discord
from discord.ext import commands

from cbusbot.gifs import GifSearchError, search_gif

log = logging.getLogger(__name__)

PATTERN = re.compile(r"\bdance\b")


class Dance(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _mentions_dance(self, message: discord.Message) -> bool:
        texts = [message.content]
        for embed in message.embeds:
            texts.extend(filter(None, (embed.title, embed.description)))
        return any(PATTERN.search(t.lower()) for t in texts)

    def _allowed(self, member: discord.Member | None) -> bool:
        if member is None:
            return False
        cfg = self.bot.config
        if member.id in (cfg.elle_id, cfg.owner_id):
            return True
        role_ids = {r.id for r in getattr(member, "roles", [])}
        return bool(role_ids & {cfg.admin_role_id, cfg.birthday_role_id})

    async def _send_twerk(self, channel) -> None:
        try:
            await channel.send(await search_gif("twerking"))
        except GifSearchError as e:
            log.warning("gif search failed: %s", e)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if self._allowed(message.author) and self._mentions_dance(message):
            await self._send_twerk(message.channel)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        # Fires when Discord attaches a gif embed after delivery. Only react
        # if the dance match is new, so we never respond twice.
        if after.author.bot:
            return
        if self._mentions_dance(before) or not self._mentions_dance(after):
            return
        if self._allowed(after.author):
            await self._send_twerk(after.channel)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dance(bot))
