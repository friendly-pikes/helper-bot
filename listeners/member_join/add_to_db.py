###############################################
#
# File: listeners.member_join.add_to_db
# Date: 09/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import *

class AddToDB(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        user = Database.userdata_conn.execute(f'SELECT * FROM user_data WHERE user_id={member.id}')
        if len(user.fetchall()) < 1:
            Database.userdata_conn.execute(f'INSERT INTO user_data VALUES (0, {member.id}, "{member.name}", "NULL", 0, 0, 0)')
        self.bot.logger.info(f"Added {member.name} to database.")

async def setup(bot):
    await bot.add_cog(AddToDB(bot))
