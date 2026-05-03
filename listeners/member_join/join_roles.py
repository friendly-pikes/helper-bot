###############################################
#
# File: listeners.member_join.join_roles
# Date: 03/03/2026 (EU)
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
from utils.semifunc import *

class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        server_cfg = files._server_cfg()
        join_roles = server_cfg['join_roles'][main_or_test(member.guild.id)]

        # Join Roles
        for rolea in join_roles:
            role = member.guild.get_role(join_roles[rolea])
            
            if role:
                # 18/03/2026 - Fixed givng bot role to users
                can_give = True
                if rolea == "bot" and member.bot == False:
                    can_give = False
                if rolea == "bots" and member.bot == False:
                    can_give = False

                try:
                    if can_give:
                        await member.add_roles(role, reason="Join Roles")
                except discord.errors.Forbidden as e:
                    self.bot.logger.warn(f"Cannot give {member.name} the role {role.name} because of a permission error - {e}")
            else:
                self.bot.logger.warn(f"Cannot give {member.name} the role {rolea} as it doesn't exist!")

async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
