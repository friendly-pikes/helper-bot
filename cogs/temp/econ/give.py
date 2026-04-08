import discord

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Give(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="give")
    async def give(self, ctx: Context, user: discord.Member, amount: int):
        """
        Give money to someone

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user you want to give money to
        amount: int
            The amount of money you want to give
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        if user.bot:
            await ctx.reply("Bots can't use the economy system.")
            return
        
        if user.id == ctx.author.id:
            await ctx.reply("You can't do that you goober! You can't give yourself your own money!")
            return

        user_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
        user_togive_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={user.id}").fetchone()

        if amount > user_data[4]:
            await ctx.reply(f"You can't give more than what you have! You have {Economy.format_amount(user_data[3])} {Economy.get_curreny_name()}.")
        else:
            new_bal = user_data[4] - amount
            new_bal_togive = user_togive_data[4] + amount
            
            Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (new_bal, ctx.author.id))
            Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (new_bal_togive, user.id))
            Database.userdata_conn.commit()

            Economy.use_econ(ctx, ctx.author, self.bot.logger)
            Economy.use_econ(ctx, user, self.bot.logger)
            await ctx.reply(f"**{ctx.author.mention} gave {Economy.format_amount(amount)} {Economy.get_curreny_name()} to {user.mention}!**")

async def setup(bot):
    await bot.add_cog(Econ__Give(bot))
