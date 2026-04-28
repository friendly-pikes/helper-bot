import re
import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class BoostMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.type == discord.MessageType.premium_guild_subscription:
            boosts_channel = msg.guild.get_channel( SemiFunc.get_channel_id(msg, "boosts") )
            total_boosts = re.sub(r'0-9:!', '', boosts_channel.topic)
            total_boosts = boosts_channel.topic.replace("Thanks for the boosts! Total boosts: ", "")

            cur_boosts = msg.guild.premium_subscription_count
            total_boosts = int(total_boosts) + 1

            # to be safe cuz of that str error.. convert to int again
            # Optimised, I know. But it's better to be more safe than sorry.
            total_boosts = int(total_boosts)
            
            # ..this also took awhile to be working and somewhat perfect.
            await boosts_channel.send(f"Thanks for boosting our server {msg.author.mention}!\nWe now have a total of {total_boosts} boosts!\n\n-# Boost image soon?! ||if we can think of one.||")
            await boosts_channel.edit(topic=f"Thanks for the boosts! Total boosts: {total_boosts}")


async def setup(bot):
    await bot.add_cog(BoostMessage(bot))
