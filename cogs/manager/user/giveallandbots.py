import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="giveallandbots", description="Give all users a role")
    async def giveallandbots(self, ctx: Context, role: discord.Role = None):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        if role:
            await ctx.reply(f"Giving everyone the `{role.name}` role.. this may take a while.", ephemeral=True)

            for user in ctx.guild.members:
                if not user.get_role(role.id):
                    await user.add_roles(role)

            # Follow up
            if ctx.interaction:
                await ctx.interaction.followup.send(f"Gave everyone the `{role.name}` role!", ephemeral=True)
            else:
                await ctx.reply(f"Gave everyone the `{role.name}` role!", ephemeral=True)
        else:
            await ctx.reply("Usage: ?giveall @role")


async def setup(bot):
    await bot.add_cog(Owner(bot))
