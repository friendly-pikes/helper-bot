###############################################
#
# File: listeners.on__ready.on_ready
# Date: 01/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################



from discord.ext import commands
from utils.discordbot import Bot


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(msg=f"")
        self.bot.logger.info(msg=f"Logged in as {self.bot.user.name}")
        # await self.bot.change_presence(status=discord.Status.invisible)
        

async def setup(bot):
    await bot.add_cog(OnReady(bot))
