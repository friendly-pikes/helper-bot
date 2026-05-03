###############################################
#
# File: cogs.staff.silly.sillinate
# Date: 01/03/2026 (EU)
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

class sillinate(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="sillinate")
    async def sillinate(self, ctx: Context, user: discord.Member):
        """
        Send someone to the sillinator!
        
        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user:
            The user to send there
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        await SemiFunc.pikesInator(self, ctx, user, "silly", "give")
        
async def setup(bot):
    await bot.add_cog(sillinate(bot))
