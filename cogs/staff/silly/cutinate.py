import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class cutinate(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="cutinate")
    async def cutinate(self, ctx: Context, user: discord.Member):
        """
        Send someone to the _ator!
        
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
            if SemiFunc.is_command_exception(ctx.author, "inator"):
                pass
            else:
                await ctx.reply("That command is staff only.")
                return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        await SemiFunc.pikesInator(self, ctx, user, "cute", "give")

async def setup(bot):
    await bot.add_cog(cutinate(bot))
