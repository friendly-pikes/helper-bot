import os
import re
import json
import random
import discord

from discord.ext import commands
from utils.discordbot import Bot

class CuteDenier9000(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        # 13/03/2026 - Bugfix: DMs can cause some issues.
        if not isinstance(msg.channel, discord.DMChannel):
            msg_content_lower = msg.content.lower()
                
            if msg_content_lower.find("not cute") >= 0 or msg_content_lower.find("nawt cute") >= 0:
                if random.randint(1, 100) > 70:
                    await msg.reply("Cute denier detected! They are undeniably cute.")

async def setup(bot):
    await bot.add_cog(CuteDenier9000(bot))