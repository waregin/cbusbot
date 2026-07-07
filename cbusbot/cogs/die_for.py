"""Replies to kiwi (or the owner) saying "I would die for ..." with euphie's meme."""

import re

import discord
from discord.ext import commands

from cbusbot.config import ROOT


class DieFor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        cfg = self.bot.config
        if message.author.id not in (cfg.kiwi_id, cfg.owner_id):
            return
        if re.search(r"\bi would die for\b", message.content.lower()):
            await message.channel.send(file=discord.File(ROOT / "kiwi.png"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DieFor(bot))
