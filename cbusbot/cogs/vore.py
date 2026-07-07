"""The v-word resets the count."""

import re

import discord
from discord.ext import commands

from cbusbot.config import ROOT


class Vore(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if not re.search(r"\bvore\b", message.content.lower()):
            return
        await message.reply("YOU RUINED IT!")
        general = self.bot.get_channel(self.bot.config.general_channel_id)
        if general is None:
            general = await self.bot.fetch_channel(self.bot.config.general_channel_id)
        await general.send(
            f"{message.author.mention} reset the count",
            file=discord.File(ROOT / "vore.png"),
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Vore(bot))
