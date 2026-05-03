###############################################
#
# File: cogs.users.misc.pingoptout
# Date: 30/04/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose: 
#  
# Author: snow2code
#
###############################################


from discord.ext import commands
from discord.errors import *
from utils.discordbot import Bot
from utils.custom.context import Context
from utils.database import Database

class UserCommands__Misc__Pingoptout(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        
    @commands.guild_only()
    @commands.hybrid_command(name="pingoptout")
    async def pingoptout(self, ctx: Context):
        """
        Opt out of random hug or boop pings from the bot

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        
        user = ctx.author
        allowed = Database.allow_ping(user.id)

        if allowed == True:
            Database.userdata_conn.execute(f'UPDATE pings SET allowed=? WHERE user_id=?', (0, user.id))
            Database.userdata_conn.commit()
            await ctx.reply("You've opted out of boop and hug pings successfully!")
        else:
            Database.userdata_conn.execute(f'UPDATE pings SET allowed=? WHERE user_id=?', (1, user.id))
            Database.userdata_conn.commit()
            await ctx.reply("You've opted in to boop and hug pings successfully!")
        
async def setup(bot):
    await bot.add_cog(UserCommands__Misc__Pingoptout(bot))
