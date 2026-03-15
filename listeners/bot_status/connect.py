import psutil
import asyncio
import discord
import platform

from datetime import datetime
from discord.ext import commands
from utils.discordbot import Bot
from utils.database import Database
from utils.semifunc import SemiFunc

def get_size(bytes, suffix="B"):
    factor = 1024
    # byte- 1024
    # gibibyte - 10
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_size__gibibyte(bytes):
    return bytes // (2**30)

async def change_message(bot: Bot):
    if bot.shutting_down == False:
        test_server = bot.get_guild(1480087423433052242)
        status_channel = test_server.get_channel(1482618083263643698)

        last_message = await status_channel.fetch_message(1482633940039630869)
                
        if last_message != None:
            uname = platform.uname()
            svmem = psutil.virtual_memory()
            node_name = uname.node

            bot_drive = None
            bot_drive_usage = None
            for i, part in enumerate(psutil.disk_partitions()):
                if part.mountpoint.startswith("D"):
                    bot_drive = part
                    bot_drive_usage = psutil.disk_usage(part.mountpoint)

            embed = bot.create_embed(
                f"🖥️ {node_name} | STATUS",
                description="Updates every minute.\n\n",
                color=discord.Color.green(),
                fields=[
                    {
                        "name": "🟢 Status",
                        "value": "Online",
                        "inline": True
                    },
                    {
                        "name": "📊 Current Metrics",
                        "value": f"• CPU: {psutil.cpu_percent()}%\n• Memory: {get_size(svmem.used)} / {get_size(svmem.available)} ({svmem.percent}%)",
                        "inline": False
                    },
                    {
                        "name": "Extra",
                        "value": f"• SSD: {get_size(bot_drive_usage.used)} / {get_size(bot_drive_usage.total)} ({bot_drive_usage.percent}%)",
                        "inline": False
                    }
                ]
            )

            embed.set_footer(text=f"Last updated: {datetime.now().strftime('%d/%m/%Y, %H:%M')}")
            embed.timestamp = datetime.utcnow()

            await last_message.edit(
                embed=embed
            )

async def loop(bot: Bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        await change_message(bot)
        await asyncio.sleep(60)

class BotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.status_check = False

    @commands.Cog.listener()
    async def on_connect(self):
        if self.status_check == False:
            self.status_check = True

            self.bot.loop.create_task(loop(self.bot))

        
        if self.bot.shutting_down == True:
            self.bot.loop.close()


async def setup(bot):
    await bot.add_cog(BotStatus(bot))


# 1482618083263643698