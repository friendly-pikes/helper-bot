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
    @commands.hybrid_command(name="nick")
    async def nick(self, ctx: Context, *, new_nick: str):
        """
        Set the bot's nickname

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        new_nick: str
            The nickname to change to for the bot
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
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        try:
            await self.bot.user.edit(nick=new_nick)
            await ctx.send(f"Changed Fluffy Helper bot's nickname to `{new_nick}`")
        except Exception as e:
            self.bot.logger.warn(e)
            await ctx.send(f"Unable to change Fluffy Helper bot's nickname. \nError:\n`{e}`")


async def setup(bot):
    await bot.add_cog(Nick(bot))
