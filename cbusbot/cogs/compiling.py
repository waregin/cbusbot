"""xkcd 303: my code's compiling."""

import re

import discord
from discord.ext import commands

from cbusbot.config import ROOT


class Compiling(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if re.search(r"\bcompiling\b", message.content.lower()):
            await message.channel.send(file=discord.File(ROOT / "compiling.png"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Compiling())
