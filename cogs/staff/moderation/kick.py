import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class kick(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="kick", description="Kick a user!")
    async def kick(self, ctx: Context, user: discord.Member = None, *, reason: str = "No reason provided."):
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
                if user.id == self.bot.user.id:
                    await ctx.reply("You can't get rid of me.")
                else:
                    await ctx.reply(f"Bots cannot be banished, banned, muted or kicked.")
                return
            
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
            await SemiFunc.moderate_user(self.bot, ctx, user, "kick", [reason])
            asyncio.sleep(0.5)
            await user.kick(reason=reason)
            await ctx.reply(f"Successfully kicked {user.name} for reason '{reason}'")
        else:
            await ctx.reply("Usage: ?ban @user long reason (This'll remove their messages from the last day)")
    
async def setup(bot):
    await bot.add_cog(kick(bot))
