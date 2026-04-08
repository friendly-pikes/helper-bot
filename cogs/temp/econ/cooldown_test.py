
from utils.econ import Economy
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class CooldownTest(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="cooldowntest")
    async def cooldowntest(self, ctx: Context):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        if Economy.econ__is_on_cooldown(ctx, ctx.author, self.bot.logger):
            await ctx.reply(f"You are on cooldown! Please try again tomorrow.")
            return
        else:
            Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)
        
        
        await ctx.reply(f"Command run ^^")

async def setup(bot):
    await bot.add_cog(CooldownTest(bot))
