import discord

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="balleaderboard")
    async def balleaderboard(self, ctx: Context):
        """
        Display the server leaderboard (top 10 users with the most money)

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        user_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data ORDER BY tokens DESC").fetchmany(10)
        top10 = []

        for user in user_data:
            if user[4] > 0:
                top10.append({
                    'name': user[2],
                    'balance': user[4]
                })

        embed: discord.Embed = Economy.econ_embed(title="Balance Leaderboard", description="View the [online leaderboard](https://fluffy-helper.page.gd/econ/leaderboard).")
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        i = 1

        for user in top10:
            field_name = f"***#{i}*** {user['name']}"
            field_content = f"`{user['balance']} {Economy.get_curreny_name()}`"
            if user['balance'] == 1:
                field_content = f"`{user['balance']} {Economy.get_curreny_name()[:6]}`"

            if i == 1:
                field_name = f"🥇 {user['name']}"
            elif i == 2:
                field_name = f"🥈 {user['name']}"
            elif i == 3:
                field_name = f"🥉 {user['name']}"

            i = i + 1
            embed.add_field(name=field_name, value=field_content, inline=False)

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Econ__Leaderboard(bot))
