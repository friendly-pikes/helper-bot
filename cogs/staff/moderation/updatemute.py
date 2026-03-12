import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class updatemute(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="updatemute", description="Update a user's mute!")
    async def updatemute(self, ctx: Context, user: discord.Member = None, duration: str = "5m"):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return
        
        if user:
            if SemiFunc.can_use_command(ctx, user, "staff"):
                await ctx.reply(f"Staff cannot be banished, banned, muted or kicked.")
                return
            if user.bot:
                await ctx.reply(f"Bots cannot be banished, banned, muted or kicked.")
                return
            
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
            if user.is_timed_out():
                if duration == 0:
                    duration = timedelta(seconds=0)
                else:
                    duration = timedelta(seconds=duration)
                    
                await SemiFunc.moderate_user(self.bot, ctx, user, "unmute", ["No reason provided for mute update."])
                await user.timeout(duration, reason=f'Time out updated by {ctx.author.name}')
                await ctx.reply(f"Sucessfully updated mute {user.mention}")
            else:
                await ctx.reply(f"The user {user.name} is not muted.")
                # /mute user:@snow2code limit: reason:
        else:
            await ctx.reply("Usage: ?updatemute @user duration")

async def setup(bot):
    await bot.add_cog(updatemute(bot))
