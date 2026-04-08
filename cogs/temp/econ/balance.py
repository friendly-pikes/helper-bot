import discord

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Balance(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="balance", aliases=["bal"])
    async def balance(self, ctx: Context, user: discord.Member = None):
        """
        Shows your balance or check the balance of someone else.

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user you want to check the balance of
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        user_real: discord.Member = ctx.author
        if user != None:
            user_real = user

        # If user is a bot. Do not check their balance
        if user_real.bot:
            await ctx.reply("Bots aren't able to use the economy system.")
            return

        not_in_db_msg = "They aren't in our user database, so we can't tell you their balance at the moment."
        have_text = user_real.name
        user_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={user_real.id}").fetchone()
        if user_real.id == ctx.author.id:
            have_text = "You have"
            not_in_db_msg = "You aren't in our user database, so we can't tell you your balance at the moment."
        else:
            have_text = user_real.name

        if len(user_data) > 0:
            balance = user_data[4]
            embed:discord.Embed = Economy.econ_embed(
                user=user_real,
                title="Balance",
                description=f"{have_text} {Economy.format_amount(round(balance, 2))} {Economy.get_curreny_name()}"
            )

            await ctx.reply(embed=embed)
        else:
            await ctx.reply(not_in_db_msg)

async def setup(bot):
    await bot.add_cog(Econ__Balance(bot))
