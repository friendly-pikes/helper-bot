###############################################
#
# File: cogs.bot_dev.misc.web_api
# Date: 30/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import os

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

import web.app as app_module

class ManagerCommands__Misc__Web(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="reloadweb")
    async def reloadweb(self, ctx: Context):
        """
        Reload the web modules

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            if SemiFunc.is_command_exception(ctx.author, "reload"):
                pass
            else:
                await ctx.reply("That command is only usable by owners and managers.")
                return
            
        app_module.reload_all()
        if os.name.lower() == "nt":
            os.system("clear")
        elif os.name.lower() == "posix":
            print("\033c")
            print("clear")
            os.system("clear")
        else:
            os.system("cls")
        print(os.name)
        msg = """
```JSON
{
    "reload_all": {
        "status": "Reloaded."
    }
    "clear_console": {
        "status": "Cleared output."
    }
}
```"""
        await ctx.reply(msg)
        
    @commands.guild_only()
    @commands.hybrid_command(name="clearconsole")
    async def clearconsole(self, ctx: Context):
        """
        Clear the terminal (Doesn't override logs)

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            if SemiFunc.is_command_exception(ctx.author, "reload"):
                pass
            else:
                await ctx.reply("That command is only usable by owners and managers.")
                return
        
        if os.name.lower() == "nt":
            os.system("clear")
        elif os.name.lower() == "posix":
            print("\033c")
            print("clear")
            os.system("clear")
        else:
            os.system("cls")
        print(os.name)
            
        await ctx.reply('```JSON\n{\n   "status": "Clear output."\n}```')
     
async def setup(bot):
    await bot.add_cog(ManagerCommands__Misc__Web(bot))
