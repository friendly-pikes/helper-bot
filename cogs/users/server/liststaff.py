import discord
import random

from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class liststaff(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="liststaff", description="Display a list of the server staff.")
    async def liststaff(self, ctx: Context):
        administrator_id = SemiFunc.get_role_id(ctx, "administrator")
        event_manager_id = SemiFunc.get_role_id(ctx, "event_manager")
        moderator_id = SemiFunc.get_role_id(ctx, "moderator")

        administrators = []
        event_managers = []
        moderators = []

        for member in ctx.guild.members:
            if member.get_role(moderator_id):
                moderators.append(f"<@{member.id}>")
            if member.get_role(administrator_id):
                # Add to administrators if not snowy (shes a server manager / server dev)
                if member.id != 888072934114074624:
                    administrators.append(f"<@{member.id}>")
            if member.get_role(event_manager_id):
                event_managers.append(f"<@{member.id}>")

        message = f"## Owner\n<@1262124659814695005>\n\n## Co Owner\n<@1267324371660177469>\n\n## Server Manager / Server Dev:\n<@888072934114074624>\n\n"
        message = f"{message}## Administrators:\n"

        for administrator in administrators:
            message = message + f"{administrator}\n"

        message = f"\n{message}## Moderators:\n"

        for moderator in moderators:
            message = message + f"{moderator}\n"

        message = f"\n{message}## Event Manager(s):\n"

        for event_manager in event_managers:
            message = message + f"{event_manager}\n"
            
        await ctx.reply(embed=self.bot.create_embed(title="Server Staff", description=message))

    # @commands.guild_only()
    # @commands.hybrid_command(name="gaydar", description="See how gay someone is!")
    # async def gaydar(self, ctx: Context, user: discord.Member):
    #     if user:
    #         if user.bot:
    #             await ctx.reply("Not able to use radar commads on bots.")
    #             return
            
    #         if SemiFunc.command_disabled(ctx):
    #             await ctx.reply("That command is currently disabled.")
    #             return
            
    #         await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
    #         embed = await SemiFunc.pikesRadar(self, user, "gay")
    #         await ctx.reply(embed=embed)
    #     else:
    #         await ctx.reply("Can't use radar commands on noone!")

async def setup(bot):
    await bot.add_cog(liststaff(bot))
