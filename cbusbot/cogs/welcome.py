"""!welcome @member... — Server Staff verify new members.

Removes the Unverified role and adds the Columbusites role for every mentioned
member. Fixes the master-branch bugs (`foreach`, Collection `.length`) that kept
the JS version from ever running.
"""

import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="welcome")
    @commands.guild_only()
    async def welcome(self, ctx: commands.Context) -> None:
        cfg = self.bot.config
        if ctx.author.get_role(cfg.staff_role_id) is None:
            return
        if not ctx.message.mentions:
            await ctx.reply("Mention the member(s) to welcome: `!welcome @someone`")
            return
        unverified = ctx.guild.get_role(cfg.unverified_role_id)
        columbusites = ctx.guild.get_role(cfg.columbusites_role_id)
        welcomed = []
        for member in ctx.message.mentions:
            if isinstance(member, discord.User):
                member = ctx.guild.get_member(member.id)
                if member is None:
                    continue
            if unverified in member.roles:
                await member.remove_roles(unverified, reason=f"!welcome by {ctx.author}")
            if columbusites not in member.roles:
                await member.add_roles(columbusites, reason=f"!welcome by {ctx.author}")
            welcomed.append(member.display_name)
        if welcomed:
            await ctx.message.add_reaction("👋")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Welcome(bot))
