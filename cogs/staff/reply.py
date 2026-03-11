import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class reply(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        
    @commands.guild_only()
    @commands.hybrid_command(name="reply", description="Send a message to whatever as a reply to a message!")
    async def reply(self, ctx: Context, channel: discord.TextChannel, message_id: str, *, message: str):
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
