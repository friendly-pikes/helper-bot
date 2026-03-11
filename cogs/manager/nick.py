import discord

from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Nick(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="nick", description="Set the bot's nickname")
    async def nick(self, ctx: Context, *, new_nick: str):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("You don't deserve me as a bot here, and you don't deserve Snowy here on earth....")
            return

        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
            
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is staff only.")
            return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        try:
            await self.bot.user.edit(nick=new_nick)
            await ctx.send(f"Changed Friendly Pikes Helper bot's nickname to `{new_nick}`")
        except Exception as e:
            self.bot.logger.warn(e)
            await ctx.send(f"Unable to change Friendly Pikes Helper bot's nickname. \nError:\n`{e}`")


async def setup(bot):
    await bot.add_cog(Nick(bot))
