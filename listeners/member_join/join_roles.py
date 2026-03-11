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
            canAdd = True
            cantAddReason = None
            if rolea == "bot":
                if member.bot == True:
                    canAdd = True
                else:
                    cantAddReason = "User is not a bot"
                    canAdd = False
            
            if canAdd:
                if role:
                    await member.add_roles(role, reason="Join Roles")
                else:
                    self.bot.logger.warn(f"Cannot give {member.name} the role {rolea} as it doesn't exist!")
            else:

                if cantAddReason != None:
                    self.bot.logger.warn(f"Cannot give {member.name} the role {rolea}. Reason is: {cantAddReason}")
                else:
                    self.bot.logger.warn(f"Cannot give {member.name} the role {rolea}. Reason is unknown.")

async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))
