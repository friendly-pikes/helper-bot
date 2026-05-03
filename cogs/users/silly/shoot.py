###############################################
#
# File: cogs.users.silly.shoot
# Date: 30/04/2026
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

class UserCommands__Silly__Shoot(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="shoot")
    async def shoot(self, ctx: Context, user: discord.Member):
        """
        Shoot someone!

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user you want the proot to shoot!
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if user.bot == True:
            await ctx.reply("I can't shoot a bot!")
            return
        
        if SemiFunc.can_use_command(ctx, user, "staff"):
            if SemiFunc.can_use_command(ctx, ctx.author, "staff"):
                pass
            else:
                await ctx.reply("I can't shoot staff!")
                return

        if user.id == ctx.author.id:
            await ctx.reply("I can't do that to you!!")
            return

        await ctx.reply(f"{user.mention}", files=[discord.File("assets/temp/shoot.png")])

async def setup(bot):
    await bot.add_cog(UserCommands__Silly__Shoot(bot))