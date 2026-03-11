import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class unbanish(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="unbanish", description="Unbanish a user!")
    async def unbanish(self, ctx: Context, user: discord.Member = None):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("It's normal to lose interest in life.. snowy has lost *ALL* interest in life...")
            return

        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)

        if user == None:
            await ctx.reply("Banish usage: ?banish @user OR use the app / slash command")
        else:
            if SemiFunc.can_use_command(ctx, user, "staff"):
                await ctx.reply(f"Staff cannot be banished, banned, muted or kicked.")
                return
            if user.bot:
                await ctx.reply(f"Bots cannot be banished, banned, muted or kicked.")
                return
            
            banishId, verifiedId = SemiFunc.get_role_id(ctx, "banished"), SemiFunc.get_role_id(ctx, "verified")
            banished, verified = ctx.guild.get_role(banishId), ctx.guild.get_role(verifiedId)

            if user.get_role(banishId):
                await user.remove_roles(banished, reason=f"They've been unbanished by {ctx.author.name}")
                await ctx.reply(f"{user.mention} has been unbanished!")
            else:
                await ctx.reply(f"Cannot unbanish {user.mention}, they aren't banished.")

async def setup(bot):
    await bot.add_cog(unbanish(bot))
