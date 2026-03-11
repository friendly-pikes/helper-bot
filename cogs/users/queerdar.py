import discord
import random

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class queerdar(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # This radar command is stolen from pride bot
    # https://github.com/Pridebot-Systems/Pridebot/blob/main/src/commands/fun/
    @commands.guild_only()
    @commands.hybrid_command(name="queerdar", description="See how queer someone is!")
    async def queerdar(self, ctx: Context, user: discord.Member):
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
        
            embed = await SemiFunc.pikesRadar(self, user, "queer")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("Can't use radar commands on noone!")

async def setup(bot):
    await bot.add_cog(queerdar(bot))
