import re
import discord
import asyncio

import utils.files as files
from datetime import datetime, timedelta
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class giverole(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="giveallandbots")
    async def giveallandbots(self, ctx: Context, role: discord.Role):
        """
        Give all users a role

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        role: discord.Role
            The role to give all users and bots
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
        
        if role:
            await ctx.reply(f"Giving everyone the `{role.name}` role.. this may take a while.", ephemeral=True)

            for user in ctx.guild.members:
                if not user.get_role(role.id):
                    await user.add_roles(role)

            # Follow up
            if ctx.interaction:
                await ctx.interaction.followup.send(f"Gave everyone the `{role.name}` role!", ephemeral=True)
            else:
                await ctx.reply(f"Gave everyone the `{role.name}` role!", ephemeral=True)
        else:
            await ctx.reply("Usage: ?giveall @role")

    @commands.guild_only()
    @commands.hybrid_command(name="giveallbutbots")
    async def giveallbutbots(self, ctx: Context, role: discord.Role):
        """
        Give all users a role

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        role: discord.Role
            The role to give all users
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        if role:
            await ctx.reply(f"Giving everyone the `{role.name}` role.. this may take a while.", ephemeral=True)

            for user in ctx.guild.members:
                if user.bot == False:
                    if not user.get_role(role.id):
                        await user.add_roles(role)

            # Follow up
            if ctx.interaction:
                await ctx.interaction.followup.send(f"Gave everyone the `{role.name}` role!", ephemeral=True)
            else:
                await ctx.reply(f"Gave everyone the `{role.name}` role!", ephemeral=True)
        else:
            await ctx.reply("Usage: ?giveall @role")

    @commands.guild_only()
    @commands.hybrid_command(name="giveallbots")
    async def giveallbots(self, ctx: Context, role: discord.Role):
        """
        Give all bots a role

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        role: discord.Role
            The role to give all bots
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        if role:
            await ctx.reply(f"Giving every bot the `{role.name}` role.. this may take a while.", ephemeral=True)

            for user in ctx.guild.members:
                if user.bot:
                    if not user.get_role(role.id):
                        await user.add_roles(role)

            # Follow up
            if ctx.interaction:
                await ctx.interaction.followup.send(f"Gave every bot the `{role.name}` role!", ephemeral=True)
            else:
                await ctx.reply(f"Gave every bot the `{role.name}` role!", ephemeral=True)
        else:
            await ctx.reply("Usage: ?giveallbots @role")

    @commands.guild_only()
    @commands.hybrid_command(name="giverole")
    async def giverole(self, ctx: Context, user: discord.Member, role: discord.Role):
        """
        Give a role to a certain user

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        user: discord.Member
            The user to give the role to
        role: discord.Role
            The role to give the member
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        if role:
            try:
                if user.get_role(role.id):
                    await ctx.reply(f"They already have the `{role.name}` role.", ephemeral=True)
                else:
                    await user.add_roles(role)
                    await ctx.reply(f"Gave {user.mention} the `{role.name}` role!", ephemeral=True)
            except commands.errors.CommandInvokeError as e:
                await ctx.reply(f"A error occured with the command <@888072934114074624>\n```{e}```")
        else:
            await ctx.reply("Usage: ?giverole @role")

async def setup(bot):
    await bot.add_cog(giverole(bot))
