###############################################
#
# File: listeners.on__message.ping_everyone
# Date: 21/02/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import re
import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class MessageEvent__PingEveryone(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        # 26/03/2026 - Bugfix: DMs can cause some issues.
        if not isinstance(msg.channel, discord.DMChannel):
            if msg.author.bot == False:
                staff_role = SemiFunc.get_role_id(msg, "staff")
                if not SemiFunc.can_use_command(msg, msg.author, "staff"):
                    if msg.mention_everyone:
                        await msg.reply("Nice try... You can't ping `@everyone`.")
                        ## Later - Add delete as needed.
                        # await msg.delete()

async def setup(bot):
    await bot.add_cog(MessageEvent__PingEveryone(bot))
