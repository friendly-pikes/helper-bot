import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class unexplode(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="unexplode", description="Take someone away from the explodinator!")
    async def unexplode(self, ctx: Context, user: discord.Member):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("You don't deserve me as a bot here, and you don't deserve Snowy here on earth....")
            return

        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        await SemiFunc.pikesInator(self, ctx, user, "explode", "remove")

async def setup(bot):
    await bot.add_cog(unexplode(bot))
