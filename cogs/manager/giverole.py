import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class giverole(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="giverole", description="Give a role to a certain user")
    async def giverole(self, ctx: Context, user: discord.Member = None, role: discord.Role = None):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("It's normal to lose interest in life.. snowy has lost *ALL* interest in life...")
            return

        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        if role:
            try:
                if user.get_role(role.id):
                    await ctx.reply(f"They already have the `{role.name}` role.", ephemeral=True)
                else:
                    await user.add_roles(role)
                    await ctx.reply(f"Gave {user.mention} the `{role.name}` role!", ephemeral=True)
            except commands.errors.CommandInvokeError as e:
                await ctx.reply(f"A error occured with the command <@888072934114074624>\n```{e}```")
        else:
            await ctx.reply("Usage: ?giverole @role")

async def setup(bot):
    await bot.add_cog(giverole(bot))
