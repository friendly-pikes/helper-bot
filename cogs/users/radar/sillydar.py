###############################################
#
# File: cogs.users.radar.sillydar
# Date: 02/03/2026 (EU)
# Date Edited: 02/03/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from typing import Union
from discord import app_commands
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class UserCommands__Radar__Sillydar(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # @commands.guild_only()
    @commands.hybrid_command(name="sillydar")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def sillydar(self, ctx: Union[Context, commands.context.Context], user: Union[discord.Member, discord.User]):
        """
        See how silly someone is!

        Parameters
        ----------
        ctx: Union[Context, commands.context.Context]
            The context of the command invocation
        user: user: Union[discord.Member, discord.User]
            The user to use the radar on
        """
        if user.bot:
            await ctx.reply("Not able to use radar commads on bots.")
            return
            
        # # if SemiFunc.command_disabled(ctx):
        # #     await ctx.reply("That command is currently disabled.")
        # #     return

        embed = await SemiFunc.pikesRadar(self.bot, user, "silly")
            
        if not isinstance(ctx.channel, discord.DMChannel):
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserCommands__Radar__Sillydar(bot))
