import os
import re
import json
import random
import discord

from datetime import datetime
from discord.ext import commands
from misc import banished_words_private as banished_words_privateA
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import SemiFunc

class BoostMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.type == discord.MessageType.premium_guild_subscription:
            boosts_channel = msg.guild.get_channel( SemiFunc.get_channel_id(msg, "boosts") )
            total_boosts = re.sub(r'0-9:!', '', boosts_channel.topic)
            # total_boosts = str(total_boosts).replace("", )

            total_boosts = boosts_channel.topic.replace("Thanks for the boosts! Total boosts: ", "")
            boosts = msg.guild.premium_subscription_count

            if total_boosts == boosts:
                total_boosts = total_boosts + 1
            # boosts_channel.edit(topic=f"Thanks for the boost! Current boosts: 16 Total boosts: 16{boosts})")
            await boosts_channel.send(f"Thanks for boosting our server {msg.author.mention}!\nWe now have a total of {total_boosts}!")

            return

async def setup(bot):
    await bot.add_cog(BoostMessage(bot))
