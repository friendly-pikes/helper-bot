###############################################
#
# File: listeners.member_joib.join_message
# Date: 07/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = member.guild.get_channel( SemiFunc.get_channel_id(member, "welcome") )

        # if files.get_config_entry("join_message_enabled"):
        await welcome_channel.send(f"Hello {member.mention}! Welcome to the server! :3")

async def setup(bot):
    await bot.add_cog(JoinMessage(bot))
