import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc


def parase_duration(duration: str):
    match = re.match(r'^(\d+)([smhd])$', duration.lower())
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)

    multipliers = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400
    }

    return value * multipliers[unit]


class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="mute", description="Mute a user!")
    async def mute(self, ctx: Context, user: discord.Member = None, duration: str = "5m", *, reason: str = "No reason provided."):
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
                    await ctx.reply("You can't get rid of my freedom!")
                else:
                    await ctx.reply(f"Bots cannot be banished, banned, muted or kicked.")
                return
            
            await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        
            errors = []

            if parase_duration(duration) > 2419200:
                duration = 2419200
                errors.append("Max duration exected! Max duration for a mute is 28 days.")
                
            if parase_duration(duration) < 0:
                duration = parase_duration("5m")
                errors.append("Duration is not a positive integer. Used 5 minutes as a replacment.")

                    
            duration = timedelta(seconds=parase_duration(duration))
                
            await SemiFunc.moderate_user(self.bot, ctx, user, "mute", [reason])
            await user.timeout(duration, reason=f'{reason} (Timed out by {ctx.author.name})')
                
            await ctx.reply(f"Sucessfully muted {user.mention} for '{reason}'")
            if len(errors) > 0:
                self.bot.logger.warn("Mute errors:")
                await ctx.send(f"Errors:", ephemeral=True)
                for error in errors:
                    self.bot.logger.warn(error)
                    await ctx.send(f"`{error}`", ephemeral=True)
        else:
            await ctx.reply("Usage: ?mute @user length (e.g 5m, 1h, 1d) long reason")

async def setup(bot):
    await bot.add_cog(Staff(bot))
