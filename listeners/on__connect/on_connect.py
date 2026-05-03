###############################################
#
# File: listeners.on__connect.on_connect
# Date: 02/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from discord.ext import commands
from utils.discordbot import Bot

class OnConnect(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        # await self.bot.change_presence(status=discord.Status.invisible)

        try:
            synced = await self.bot.tree.sync()
            self.bot.logger.info(msg=f"Synced {len(synced)} commands globally.")
        except Exception as e:
            self.bot.logger.error(msg=f"Error: {e}")

async def setup(bot):
    await bot.add_cog(OnConnect(bot))
