import random

from typing import Literal
from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc
    
class Econ__Cups(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="cups")
    async def cups(self, ctx: Context, cup: Literal[1, 2, 3, 4], bet: int):
        """
        Pick the cup that is hiding the coin. Choose 1, 2, 3, or 4

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        cup: Literal[1, 2, 3, 4]
            TThe cup you think the coin is under.
        bet: int
            The amount you want to wager.
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        user = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
        if bet > user[4] or user[4] == 0:
            await ctx.reply(f"You don't have enough to bet.")
            return
        Economy.use_econ(ctx, ctx.author, self.bot.logger)
        
        if Economy.econ__is_on_cooldown(ctx, ctx.author, self.bot.logger):
            await ctx.reply(f"You are on cooldown! Please try again tomorrow.")
            return

        if bet < 1:
            bet = 1

        rand_cup = random.randint(1, 4)
        you_won = False
        
        if cup == rand_cup:
            you_won = True
            bal_addition = bet * 2

        if you_won:
            # "Congratulations You Won!"
            if len(user) > 0:
                bal = user[4]
                embed = Economy.econ_embed(
                        user=ctx.author,
                        title=f"Cups",
                        description=f"Congrats, coin was under cup {cup}!\n\nYou won {bal_addition} {Economy.get_curreny_name()}!"
                )

                Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (bal + bal_addition, ctx.author.id))
                Database.userdata_conn.commit()
                await ctx.reply(embed=embed)
            else:
                embed = Economy.econ_embed(
                        user=ctx.author,
                        title=f"Cups",
                        description=f"Congrats, coin was under cup {cup}!\nYou won {bal_addition} {Economy.get_curreny_name()}!\n\n..but it can't be added to your balance, as you aren't registed in the database."
                )

                await ctx.reply(embed=embed)
        else:
            embed = Economy.econ_embed(
                    user=ctx.author,
                    title=f"Cups",
                    description=f"Sorry, the coin was under cup {rand_cup}.\nYou lost your {Economy.get_curreny_name()}."
            )

            await ctx.reply(embed=embed)

        Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)


async def setup(bot):
    await bot.add_cog(Econ__Cups(bot))
