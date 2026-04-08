import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class SetStatus(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="setstatus")
    async def setstatus(self, ctx: Context, *, message: str = "I hungy. gimme ram :3"):
        """
        Set the bots status

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        message: str
            The message in the status
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
        
        activity = discord.CustomActivity(name=message)
        
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        await ctx.reply(f"Set bot's status to `{message}`.\n..even though it's gonna change in like a minute or something.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(SetStatus(bot))
