import discord

from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="announce")
    async def announce(self, ctx: Context, channel: discord.TextChannel, *, message: str):
        """
        Send a message to a channel as a embed

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        message: str
            The description of the embed
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
            await channel.send(embed=self.bot.create_embed_notitle(description=message, color=discord.Color.pink(), use_by_snow2code_footer=True))
            await ctx.send("Sent message successfully!")
        except Exception as e:
            self.bot.logger.warn(e)


async def setup(bot):
    await bot.add_cog(Announce(bot))
