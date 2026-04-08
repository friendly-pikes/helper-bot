
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class UserCommands__server__Serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="serverinfo")
    async def serverinfo(self, ctx: Context):
        """
        Display the server stats (total members, total bots, etc)

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
        
        members = 0
        bots = 0
        roles = len(ctx.guild.roles)
        # len(ctx.guild.categories)
        creation_date = ctx.guild.created_at.strftime("%d/%m/%Y %H:%M")

        for member in ctx.guild.members:
            if member.bot == False:
                members = members + 1
            else:
                bots = bots + 1

        embed = self.bot.create_embed_notitle(
            description="",
            fields=[
                {
                    "name": "Owner",
                    "value": ctx.guild.owner.display_name,
                    "inline": True,
                },
                {
                    "name": "Members",
                    "value": members,
                    "inline": True,
                },
                {
                    "name": "Bots",
                    "value": bots,
                    "inline": True,
                },
                {
                    "name": "Roles",
                    "value": roles,
                    "inline": True,
                }
                # {
                #     "name": "",
                #     "value": roles,
                #     "inline": True,
                # },
            ]
        )
        
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"ID: {ctx.guild.id} | Server Created: {creation_date} • Bot developed by snow2code")

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(UserCommands__server__Serverinfo(bot))
