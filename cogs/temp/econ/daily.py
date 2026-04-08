import utils.files as files

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Daily(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="daily")
    async def daily(self, ctx: Context):
        """
        Claim your daily reward.

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
        
        if Economy.econ__is_on_cooldown(ctx, ctx.author, self.bot.logger):
            await ctx.reply("You've already claimed your daily reward.. you can claim your next daily reward in {whatever time}.")
        else:
            user = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()

            Economy.use_econ(ctx, ctx.author, self.bot.logger)

            amount = files.get_config_entry("daily_reward")
            bal = user[4]

            Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (bal + amount, ctx.author.id))
            Database.userdata_conn.commit()
            embed = Economy.econ_embed(
                title="Daily Reward Claimed",
                description=f"+{amount} {Economy.get_curreny_name()}",
                user=ctx.author
                ## I.. I am too lazy to get this up and running..
                # fields=[
                #     {
                #         'name': 'Streak',
                #         'value': ""
                #     }
                # ]
            )

            await ctx.reply(embed=embed)
            Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)
        
async def setup(bot):
    await bot.add_cog(Econ__Daily(bot))
