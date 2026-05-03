###################################################
#
# File: listeners.on__message.forward_suggestion
# Date: 17/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###################################################


import discord

from discord.ext import commands
from utils.discordbot import Bot

class ForwardSuggestion(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        test_guild = self.bot.get_guild(1480087423433052242)
        suggestions_forwardto = test_guild.get_channel(1483635665727000686)
        
        if msg.channel.id in [1483755129059409920, 1479736151203123280]:
            await suggestions_forwardto.send(f"{msg.author.mention} suggests: {msg.content}")

async def setup(bot):
    await bot.add_cog(ForwardSuggestion(bot))