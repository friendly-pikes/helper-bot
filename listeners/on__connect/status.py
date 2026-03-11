import random
import asyncio
import discord

from discord.ext import commands
from utils.discordbot import Bot

import utils.files as files
from utils.semifunc import SemiFunc

prev_status = []

async def change_status(bot: Bot):
    statuses = files._config()['statuses']
    rand_status = random.choice(statuses)
    activity = -1

    if len(prev_status) > 5:
        prev_status.clear()

    if rand_status['message'] in prev_status:
        await change_status(bot)
        return

    if rand_status['activity'] == 'unknown' or rand_status['activity'] == 'None':
        activity = -1
    elif rand_status['activity'] == 'playing':
        activity = discord.Activity(type=discord.ActivityType.playing, name=rand_status['message'])
    elif rand_status['activity'] == 'streaming':
        activity = discord.Activity(type=discord.ActivityType.streaming, name=rand_status['message'])
    elif rand_status['activity'] == 'listening':
        activity = discord.Activity(type=discord.ActivityType.listening, name=rand_status['message'])
    elif rand_status['activity'] == 'watching':
        activity = discord.Activity(type=discord.ActivityType.watching, name=rand_status['message'])
    elif rand_status['activity'] == 'custom':
        activity = discord.CustomActivity(name=rand_status['message'])
    else:
        activity = -1
            
    # print(f"Change status to: {rand_status['message']}")
    prev_status.append(rand_status['message'])
    await bot.change_presence(status=discord.Status.online, activity=activity)

async def status_loop(bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        await change_status(bot)
        await asyncio.sleep(70)
        # 120
        # 60

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        
        # 09/03/2026 - Random statuses
        # await change_status(self.bot)
        # self.bot.loop.create_task(status_loop(self.bot))
        await self.bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="It's normal to lose interest in life.. snowy has lost *ALL* interest in life..."))

async def setup(bot):
    await bot.add_cog(Status(bot))
