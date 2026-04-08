import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class UserCommands__Radar__Sillydar(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="sillydar")
    async def sillydar(self, ctx: Context, user: discord.Member):
        """
        See how silly someone is!

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user to use the radar on
        """
        if user:
            if user.bot:
                await ctx.reply("Not able to use radar commads on bots.")
                return
            
            if SemiFunc.command_disabled(ctx):
                await ctx.reply("That command is currently disabled.")
                return
            
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
            embed = await SemiFunc.pikesRadar(self.bot, user, "silly")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("Can't use radar commands on noone!")

async def setup(bot):
    await bot.add_cog(UserCommands__Radar__Sillydar(bot))
