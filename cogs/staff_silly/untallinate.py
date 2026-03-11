import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class untallinate(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="untallinate", description="Take someone away from the tallinator!")
    async def untallinate(self, ctx: Context, user: discord.Member):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("It's normal to lose interest in life.. snowy has lost *ALL* interest in life...")
            return

        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        await SemiFunc.pikesInator(self, ctx, user, "tall", "remove")

async def setup(bot):
    await bot.add_cog(untallinate(bot))
