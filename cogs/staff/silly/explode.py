###############################################
#
# File: cogs.staff.silly.explode
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

class explode(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="explode")
    async def explode(self, ctx: Context, user: discord.Member):
        """
        Send someone to the explodinator!
        
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

        await SemiFunc.pikesInator(self, ctx, user, "explode", "give")

async def setup(bot):
    await bot.add_cog(explode(bot))
