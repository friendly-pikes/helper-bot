import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class SetStatus(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="setstatus", description="dsg")
    async def setstatus(self, ctx: Context, message: str = "I hungy. gimme ram :3"):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("It's normal to lose interest in life.. snowy has lost *ALL* interest in life...")
            return

        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        activity = discord.CustomActivity(name=message)
                
        # print(f"Change status to: {rand_status['message']}")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.reply(f"Set bot's status to `{message}`.\n..even though it's gonna change in like a minute or something.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(SetStatus(bot))
