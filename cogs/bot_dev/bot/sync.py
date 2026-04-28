
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

async def sync_commands(self, ctx: Context):
    try:
        synced = await self.bot.tree.sync()
        await ctx.reply(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        self.bot.logger.error(msg=f"Error: {e}")

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="syncjobs")
    async def syncjobs(self, ctx: Context):
        """
        Sync the job list from the database

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
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
        
        SemiFunc.update_jobs(self.bot.logger)
        await ctx.reply(f"Updating the job list in the background. This won't be displayed besides from this message.")


    @commands.guild_only()
    @commands.hybrid_command(name="sync")
    async def sync(self, ctx: Context):
        """
        Sync the bot's commands

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
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
        
        await sync_commands(self, ctx)

    @commands.guild_only()
    @commands.hybrid_command(name="syncafkusers")
    async def syncafkusers(self, ctx: Context):
        """
        Sync AFK users from the database.

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
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
        
        SemiFunc.update_afk(self.bot.logger)
        await ctx.reply(f"Syncing AFK Users in the background. This won't be displayed besides from this message.")

    @commands.guild_only()
    @commands.hybrid_command(name="syncbanishedlist")
    async def syncbanishedlist(self, ctx: Context):
        """
        Sync the banished list from the database

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
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
        
        SemiFunc.update_banished(self.bot.logger)
        await ctx.reply(f"Updating the banished list in the background. This won't be displayed besides from this message.")

async def setup(bot):
    await bot.add_cog(Sync(bot))
