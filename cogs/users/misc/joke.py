###############################################
#
# File: cogs.users.misc.joke
# Date: 30/04/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose: 
#  
# Author: chilly_dafur
#
###############################################


import discord
from discord.ext import commands

from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semibot import SemiBot
from utils.semifunc import SemiFunc

class UserCommands__Misc__Joke(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_command(name="joke") #, aliases=["telljoke"])
    
    # 30/04/2026 snow2code: maybe just in the server for now?
    @commands.guild_only()
    async def joke(self, ctx: Context):
        """
        Tells a random joke!
        
        Parameters
        ----------
        ctx: Context
            The context of the command ivokation
        """

        # 30/04/2026 snow2code: this'll flood the console with command logs for jokes.. we don't want that, now do we?
        if not isinstance(ctx.channel, discord.DMChannel):
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.context, ctx.interation, ctx)

        selected_joke = SemiBot.get_joke()

        await ctx.send(selected_joke)

async def setup(bot):
    await bot.add_cog(UserCommands__Misc__Joke(bot))