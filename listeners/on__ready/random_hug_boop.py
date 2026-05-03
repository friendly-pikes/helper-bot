###############################################
#
# File: listeners.on__ready.random_hug_boop
# Date: 30/04/2026
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import random
import discord
import asyncio

from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import SemiFunc
from utils.database import Database

class RandomHugBoop(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.randomly_huggin_var = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.randomly_huggin_var == False:
            self.randomly_huggin_var = True
            self.bot.loop.create_task(self.randomly_huggin())

    async def randomly_huggin(self):
        bot = self.bot
        config = files._bot_config()
        await bot.wait_until_ready()

        while not bot.is_closed():
            await asyncio.sleep(3600) # Final
            # await asyncio.sleep(5) # Testing time
            
            # guild = bot.get_guild( config['test_server_id'] )
            guild = bot.get_guild( config['main_server_id'] )
            
            members = []

            # 02/05/2024, snowy: Other code didn't work out...
            for member in guild.members:
                if member.bot:
                    continue

                if Database.allow_ping(member.id) == False:
                    continue

                # Let's be respectable. If using offline, invisible or DND status, reroll
                if member.status in [discord.Status.offline, discord.Status.invisible, discord.Status.dnd]:
                    continue

                members.append(member)

            random_member = random.choice(members)

            choice = random.choice(["hug", "boop"])
            general_chat_id = SemiFunc.get_channel_id(guild.id, "general-chat")
            # general_chat_id = 1491887133236138235
            general_chat = guild.get_channel(general_chat_id)
            await general_chat.send(f"{random_member.mention} ***{choice}***\n-# Opt out of this with ?pingoptout or /pingoptout in <#1477493580061741156>")

async def setup(bot):
    await bot.add_cog(RandomHugBoop(bot))
