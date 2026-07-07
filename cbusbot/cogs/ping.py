import discord
from discord import app_commands
from discord.ext import commands


class Ping(commands.Cog):
    """Trivial end-to-end command: /ping slash command, plus the legacy
    behavior of replying "pong" to a bare "ping" message."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check that CbusBot is alive")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"pong ({round(self.bot.latency * 1000)}ms)"
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        if message.content.lower() == "ping":
            await message.reply("pong")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
