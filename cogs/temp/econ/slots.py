import discord
import random

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Slots(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="slots")
    async def slots(self, ctx: Context, bet: int=100):
        """
        Spin the slot machine

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
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
        
        if Economy.econ__is_on_cooldown(ctx, ctx.author, self.bot.logger):
            await ctx.reply(f"You are on cooldown! Please try again tomorrow.")
            return
        
        user = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
        if bet > user[4] or user[4] == 0:
            await ctx.reply(f"You don't have enough to bet.")
            return
        Economy.use_econ(ctx, ctx.author, self.bot.logger)
        
        if bet < 100:
            await ctx.reply(f"You need to wager atleast 100 {Economy.get_curreny_name()}")
            return
        if bet > 1000:
            await ctx.reply(f"Max bet is 1000 {Economy.get_curreny_name()}")
            return
        

        times_factors = random.randint(1, 5)
        earning = int(bet * times_factors)

        final = []

        for i in range(3):
            # Probably a good idea to edit those for our bot-
            a = random.choice(["❄️", "💎", "💰"])
            final.append(a)

        win = False
        multiplier = 0
        earning = 0
        new_bal = 0

        # All 3 match
        # print(?rfinal)
        if final[0] == final[1] == final[2]:
            win = True
            multiplier = random.randint(3, 5)
            
        elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
            win = True
            multiplier = random.uniform(1.2, 2)
        
        if win:
            earning = int(bet * multiplier)
            new_bal = user[4] + earning
        else:
            earning = -bet
            new_bal = user[4] - bet

        Database.userdata_conn.cursor().execute(f"UPDATE user_data SET tokens=? WHERE user_id=?", (new_bal, ctx.author.id))
        Database.userdata_conn.commit()

        embed = discord.Embed(title=f"Slot Machine", color=discord.Color.green())

        if earning < 0:
            embed.color = discord.Color.red()
            embed.add_field(name=f"You Won {earning}", value=f"{final}")
            embed.add_field(name=f"-------------", value=f"**Multiplier** x{times_factors}", inline=False)
            embed.add_field(name=f"-------------", value=f"**New Balance** {new_bal} credits", inline=False)
        else:
            embed.add_field(name=f"You Won {earning}", value=f"{final}")
            embed.add_field(name=f"-------------", value=f"**Multiplier** x{times_factors}", inline=False)
            embed.add_field(name=f"-------------", value=f"**New Balance** {new_bal} credits", inline=False)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
        await ctx.reply(embed=embed)

        Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)


async def setup(bot):
    await bot.add_cog(Econ__Slots(bot))
