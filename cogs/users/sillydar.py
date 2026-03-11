import discord
import random

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class sillydar(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="sillydar", description="See how sillydar someone is!")
    async def sillydar(self, ctx: Context, user: discord.Member):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("It's normal to lose interest in life.. snowy has lost *ALL* interest in life...")
            return

        if user:
            if user.bot:
                await ctx.reply("Not able to use radar commads on bots.")
                return
            
            if SemiFunc.command_disabled(ctx):
                await ctx.reply("That command is currently disabled.")
                return
            
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
            embed = await SemiFunc.pikesRadar(self, user, "silly")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("Can't use radar commands on noone!")

async def setup(bot):
    await bot.add_cog(sillydar(bot))
