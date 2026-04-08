
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="blackjack")
    async def blackjack(self, ctx: Context):
        """
        Play a game of blackjack with an optional perfect pair side bet.

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return

        await ctx.reply(
            content="Because snowy is stoopid, blackjack isn't available.\nComplain to her about this, noone else.\n..feel free to try and code this for the bot though. Just don't use AI.. for our sake. We don't want to be like Dammy...",
            ephemeral=True
        )
        
async def setup(bot):
    await bot.add_cog(Econ__Blackjack(bot))
