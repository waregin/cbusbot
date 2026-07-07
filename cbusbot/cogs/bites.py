"""SHE NO BITE!!"""

import re

import discord
from discord.ext import commands

PATTERN = re.compile(r"\b(she|cosette|cossete) bite\b")


class Bites(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if PATTERN.search(message.content.lower()):
            await message.reply("SHE NO BITE!!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bites())
