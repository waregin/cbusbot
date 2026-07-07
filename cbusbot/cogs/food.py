"""Every channel is food channel."""

import random

import discord
from discord.ext import commands

from cbusbot.config import ROOT


class Food(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.mention_everyone:
            return
        if not any(c.id == self.bot.config.food_channel_id for c in message.channel_mentions):
            return
        if random.random() < 0.5:
            await message.channel.send(file=discord.File(ROOT / "food.png"))
        else:
            await message.channel.send("Every channel is food channel")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Food(bot))
