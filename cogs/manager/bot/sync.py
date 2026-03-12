
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
    @commands.hybrid_command(name="sync", description="Sync the bot's commands")
    async def sync(self, ctx: Context):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        await sync_commands(self, ctx)

    @commands.guild_only()
    @commands.hybrid_command(name="syncafkusers", description="Sync AFK users from the database.")
    async def syncafkusers(self, ctx: Context):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        SemiFunc.update_afk(self.bot.logger)
        await ctx.reply(f"Syncing AFK Users in the background. This won't be displayed besides from this message.")

    @commands.guild_only()
    @commands.hybrid_command(name="syncbanishedlist", description="Sync the banished list from the database")
    async def syncbanishedlist(self, ctx: Context):
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        SemiFunc.update_banished(self.bot.logger)
        await ctx.reply(f"Updating the banished list in the background. This won't be displayed besides from this message.")

async def setup(bot):
    await bot.add_cog(Sync(bot))
