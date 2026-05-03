###############################################
#
# File: cogs.bot_dev.bot.shutdown
# Date: 27/03/2026(?) (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class ManagerCommands__Bot__Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="shutdown")
    async def shutdown(self, ctx: Context):
        """
        And now I'll wave, so long! -- Placeholder

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager_only"):
            if SemiFunc.is_command_exception(ctx.author, "reload"):
                pass
            else:
                await ctx.reply("That command is only usable by the server manager / server dev.")
                return
        
        # Scrapped idea: Lethal Company Life Support Offline gif.. custom made / remade.
        await ctx.reply("Life support offline.")
        self.bot.close()
        
        
            

async def setup(bot):
    await bot.add_cog(ManagerCommands__Bot__Shutdown(bot))
