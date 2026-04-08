import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class reply(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        
    @commands.guild_only()
    @commands.hybrid_command(name="reply")
    async def reply(self, ctx: Context, channel: discord.TextChannel, message_id: str, *, message: str):
        """
        Send a message to whatever as a reply to a message!
        
        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        message_id: str
            The message id of message to send whatever message to as a reply
        message: str
            The message to use as a reply to the message id
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        if ctx.channel.id == SemiFunc.get_channel_id(ctx, "staff_commands"):
            message_id = int(message_id)
            msg_reply = await channel.fetch_message(message_id)
            if msg_reply:
                await msg_reply.reply(message)
                await ctx.reply("Sent message successfully!", ephemeral=True)
            else:
                await ctx.reply(f"Cannot find a message with the id '{message_id}' in {channel.mention}")
        else:
            await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(reply(bot))
