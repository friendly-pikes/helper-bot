
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class UserCommands__server__Liststaff(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="liststaff")
    async def liststaff(self, ctx: Context):
        """
        Display a list of the server staff

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if ctx.channel.id != SemiFunc.get_channel_id(ctx, 'bot-commands'):
            # Use in bot commands you goober
            await ctx.reply("Use that command in <#1477493580061741156>")
            return

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

async def setup(bot):
    await bot.add_cog(UserCommands__server__Liststaff(bot))
