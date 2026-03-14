import random
import asyncio
import discord

from discord.ext import commands
from utils.discordbot import Bot

import utils.files as files
from utils.semifunc import SemiFunc

prev_status = []

async def change_status(bot: Bot):
    rand = random.randint(1, 100)
    if rand > 80:
        general_main = bot.get_channel(1414222708324958385)
        reaction = bot.get_emoji(1479235584127143978)

        await general_main.send(content=f"<:{reaction.name}:{reaction.id}>")


async def status_loop(bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        await asyncio.sleep(960)
        await change_status(bot)
        # 360 - 6 minutes
        # 240 - 4 minutes
        # 180 - 3 minutes
        # 120 - 2 minutes
        # 60 - 1 minute

class OWO(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.owo = False

    @commands.Cog.listener()
    async def on_connect(self):
        if self.owo == False:
            self.owo = True
            # await change_status(self.bot)
            self.bot.loop.create_task(status_loop(self.bot))
            # await self.bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="It's normal to lose interest in life.. snowy has lost *ALL* interest in life..."))

async def setup(bot):
    await bot.add_cog(OWO(bot))
