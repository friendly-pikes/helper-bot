###############################################
#
# File: cogs.users.radar.transdar
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

class UserCommands__Radar__Transdar(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # This radar command is stolen from pride bot
    # https://github.com/Pridebot-Systems/Pridebot/blob/main/src/commands/fun/
    # @commands.guild_only()
    @commands.hybrid_command(name="transdar")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def transdar(self, ctx: Union[Context, commands.context.Context], user: Union[discord.Member, discord.User]):
        """
        See how trans someone is!

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

        embed = await SemiFunc.pikesRadar(self.bot, user, "trans")
            
        if not isinstance(ctx.channel, discord.DMChannel):
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserCommands__Radar__Transdar(bot))
