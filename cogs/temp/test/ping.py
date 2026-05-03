###############################################
#
# File: cogs.temp.test.ping
# Date: Around 09/04/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import os
import discord
import requests

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc
from utils.semibot import SemiBot

class Test__Ping(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: Context):
        """
        Get bot ping

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        ping = f"{round(self.bot.latency * 1000)}ms"
        
        await ctx.reply(f"Pong.\nBot ping: {ping}")
        
async def setup(bot):
    await bot.add_cog(Test__Ping(bot))
