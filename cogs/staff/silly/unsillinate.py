###############################################
#
# File: cogs.staff.silly.unsillinate
# Date: 02/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class unsillinate(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="unsillinate")
    async def unsillinate(self, ctx: Context, user: discord.Member):
        """
        Take someone away form the sillinator!
        
        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user:
            The user to take away from there
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        await SemiFunc.pikesInator(self, ctx, user, "silly", "remove")
    
async def setup(bot):
    await bot.add_cog(unsillinate(bot))
