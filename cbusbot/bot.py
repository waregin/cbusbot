import logging

import discord
from discord.ext import commands

from cbusbot.config import Config

log = logging.getLogger(__name__)


class CbusBot(commands.Bot):
    def __init__(self, config: Config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.config = config

    async def setup_hook(self) -> None:
        for cog in self.config.enabled_cogs:
            await self.load_extension(f"cbusbot.cogs.{cog}")
            log.info("Loaded cog: %s", cog)
        # Sync slash commands to the home guild only — instant, no global propagation delay.
        guild = discord.Object(id=self.config.guild_id)
        self.tree.copy_global_to(guild=guild)
        synced = await self.tree.sync(guild=guild)
        log.info("Synced %d slash command(s) to guild %s", len(synced), self.config.guild_id)

    async def on_ready(self) -> None:
        log.info("Logged in as %s (id %s)", self.user, self.user.id)
