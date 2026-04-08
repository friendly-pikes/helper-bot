import enum
import random

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Sides(str, enum.Enum):
    heads = "heads"
    tails = "tails"
    
class Econ__Coin(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="coin")
    async def coin(self, ctx: Context, choice: Sides, bet: int):
        """
        Bet on heads or tails.

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        choice: Sides
            The side you think the coin will land on.
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

        rand_side = random.choice([1, 0])
        you_won = False
        
        if rand_side == 1 and choice.value == Sides.heads.value:
            you_won = True
            bal_addition = bet * 2
        if rand_side == 0 and choice.value == Sides.tails.value:
            you_won = True
            bal_addition = bet * 2

        if you_won:
            # "Congratulations You Won!"
            if len(user) > 0:
                bal = user[4]
                embed = Economy.econ_embed(
                        user=ctx.author,
                        title=f"{choice.value.capitalize()}!",
                        description=f"Congrats, the coin landed on {choice.value}!\nYou won {bal_addition} {Economy.get_curreny_name()}!"
                )

                Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (bal + bal_addition, ctx.author.id))
                Database.userdata_conn.commit()
                await ctx.reply(embed=embed)
            else:
                embed = Economy.econ_embed(
                        user=ctx.author,
                        title=f"{choice.value.capitalize()}!",
                        description=f"Congrats, the coin landed on {choice.value}!\nYou won {bal_addition} {Economy.get_curreny_name()}!\n\n..but it can't be added to your balance, as you aren't registed in the database."
                )

                await ctx.reply(embed=embed)
        else:
            side = "heads"
            if rand_side == 0:
                side = "tails"
                
            embed = Economy.econ_embed(
                    user=ctx.author,
                    title=f"{side.capitalize()}!",
                    description=f"Sorry, the coin landed on {side}.\nYou lost your {Economy.get_curreny_name()}."
            )

            await ctx.reply(embed=embed)

        Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)

async def setup(bot):
    await bot.add_cog(Econ__Coin(bot))
