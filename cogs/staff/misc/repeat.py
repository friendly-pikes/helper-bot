import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class repeat(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="repeat")
    async def repeat(self, ctx: Context, channel: discord.TextChannel, message: str):
        """
        Send a message to whatever channel!
        
        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        channel: discord.TextChannel
            The channel to send the message to
        message: str
            The message to send to the channel
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return

        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        if ctx.channel.id == SemiFunc.get_channel_id(ctx, "staff_commands"):
            await channel.send(message)
            await ctx.reply("Sent message successfully!", ephemeral=True)
        else:
            await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(repeat(bot))
