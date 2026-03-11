import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class unmute(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="unmute", description="Unmute a user!")
    async def unmute(self, ctx: Context, user: discord.Member = None, *, reason: str = "No reason provided."):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("It's normal to lose interest in life.. snowy has lost *ALL* interest in life...")
            return

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
                duration = timedelta(seconds=0)
                await SemiFunc.moderate_user(self.bot, ctx, user, "unmute", [reason])
                await user.timeout(duration, reason=f'{reason} (Timed out by {ctx.author.name})')
                await ctx.reply(f"Sucessfully unmuted {user.mention} for '{reason}'")
                # /mute user:@snow2code limit: reason:
            else:
                await ctx.reply(f"`{user.name}` cannot be unmuted")
        else:
            await ctx.reply("Usage: ?unmute @user long reason")

async def setup(bot):
    await bot.add_cog(unmute(bot))
