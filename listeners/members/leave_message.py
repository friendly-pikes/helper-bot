###############################################
#
# File: listeners.members.leave_message
# Date: 05/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import SemiFunc

class OnMemberLeave(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        # Unused for now
        pass
    
        # gen_chat = member.guild.get_channel( SemiFunc.get_channel_id(member, "general-chat") )
        
        # if files.get_config_entry("leave_message_enabled"):
        #     gen_chat.send(f"User {member.name} left {member.guild.name} ;w;\nWe hope you had a wonderful stay, sorry that you had to leave!")

async def setup(bot):
    await bot.add_cog(OnMemberLeave(bot))
