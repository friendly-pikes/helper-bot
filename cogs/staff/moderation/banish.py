import re
import discord

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class banish(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="banish")
    async def banish(self, ctx: Context, user: discord.Member, *, reason: str):
        """
        Banish a user!
        
        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user to banish
        reason: str
            The reason why they got banished
        """
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
                if user.id == self.bot.user.id:
                    await ctx.reply("You can't get rid of me.")
                else:
                    await ctx.reply(f"Bots cannot be banished, banned, muted or kicked.")
                return
            
            banishId, verifiedId = SemiFunc.get_role_id(ctx, "banished"), SemiFunc.get_role_id(ctx, "verified")
            banished, verified = ctx.guild.get_role(banishId), ctx.guild.get_role(verifiedId)

            if user.get_role(banishId):
                await ctx.reply(f"Cannot banish {user.mention}, they are already banished.\nUnbanish them with `unbanish`")
            else:
                await SemiFunc.moderate_user(self.bot, ctx, user, "banish", [reason])
                await user.remove_roles(verified, reason=f"They've been banished by {ctx.author.name}")
                await user.add_roles(banished, reason=f"They've been banished by {ctx.author.name} for the reason `{reason}`")
                await ctx.reply(f"{user.mention} has been banished!\nReason: `{reason}`")

async def setup(bot):
    await bot.add_cog(banish(bot))
