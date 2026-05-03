###############################################
#
# File: cogs.temp.econ.steal
# Date: 17/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import random
import discord

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Steal(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="steal")
    async def steal(self, ctx: Context, user: discord.Member):
        """
        Steal money from someone

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user you want to steal from
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

        if user.id == ctx.author.id:
            await ctx.reply(f"You can't rob yourself.")
            return
        
        if user.bot:
            await ctx.reply("Bots can't use the economy system.")
            return

        success_rate = 50

        # Funnies. snowy and natalie has a 70% chance of a successful theft
        if ctx.author.id == 888072934114074624 or ctx.author.id == 1094359688541372457:
            success_rate = 70

        if random.randint(1, 100) < success_rate:
            amount = random.randint(5, 10)
            user_bal = Database.userdata_conn.execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()[4]
            user_steal_bal = Database.userdata_conn.execute(f"SELECT * FROM user_data WHERE user_id={user.id}").fetchone()[4]

            if user_steal_bal == 0:
                await ctx.reply("They don't have anything for you to steal.")
                return
            else:
                if user_steal_bal == amount:
                    amount = user_steal_bal

            Database.userdata_conn.execute(f"UPDATE user_data SET tokens=? WHERE user_id=?", (user_steal_bal - amount, user.id))
            Database.userdata_conn.execute(f"UPDATE user_data SET tokens=? WHERE user_id=?", (user_bal + amount, ctx.author.id))
            Database.userdata_conn.commit()

            try:
                await user.send(f"{ctx.author.mention} ({ctx.author.name}) stole {amount} {Economy.get_curreny_name()} from you!")
            except discord.Forbidden:
                self.bot.logger.info(f"Unable to DM {user.name} to let them know that {ctx.author.name} stole {amount} {Economy.get_curreny_name()} from them.")
            await ctx.reply(f"You successfully stole {amount} {Economy.get_curreny_name()} from {user.mention}!")
        else:
            data = Database.userdata_conn.execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
            bal = data[4]
            fine = random.randint(2, 7)

            if fine > bal:
                fine = bal
            
            Database.userdata_conn.execute(f"UPDATE user_data SET tokens=? WHERE user_id=?", (bal - fine, ctx.author.id))
            Database.userdata_conn.commit()
            await ctx.reply(f"You were caught trying to rob {user.mention} and got fined {str(fine)} {Economy.get_curreny_name()}.")
        Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)

async def setup(bot):
    await bot.add_cog(Econ__Steal(bot))
