"""Replies when the bot is @mentioned: inspire pic, owner greeting, or fleshbags."""

import random
import re

import discord
from discord.ext import commands

from cbusbot.config import ROOT

INSPIRE_DIR = ROOT / "inspirePics"


class Mentions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or message.mention_everyone:
            return
        if self.bot.user not in message.mentions:
            return
        if re.search(r"\binspire\b", message.content.lower()):
            chosen = random.choice(list(INSPIRE_DIR.iterdir()))
            await message.channel.send(file=discord.File(chosen))
        elif message.author.id == self.bot.config.owner_id:
            await message.reply("Your wish is my command")
        else:
            await message.reply("Greetings fleshbags!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Mentions(bot))
