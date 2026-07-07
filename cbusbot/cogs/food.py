"""Every channel is food channel.

Alternates strictly between the image and the words (random starting side)
instead of rolling independently each time — independent rolls produce
streaks (a run of 5 images is a 1-in-32 event, and it *will* happen),
which reads as "the bot only ever posts the image".
"""

import random

import discord
from discord.ext import commands

from cbusbot.config import ROOT


class Food(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.show_image = random.random() < 0.5

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.mention_everyone:
            return
        if not any(c.id == self.bot.config.food_channel_id for c in message.channel_mentions):
            return
        if self.show_image:
            await message.channel.send(file=discord.File(ROOT / "food.png"))
        else:
            await message.channel.send("Every channel is food channel")
        self.show_image = not self.show_image


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Food(bot))
