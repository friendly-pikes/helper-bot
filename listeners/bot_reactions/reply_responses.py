###############################################
#
# File: listeners.bot_reactions.reply_responses
# Date: 27/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.files import *
from utils.semifunc import SemiFunc

responses = [
    # {
    #     "search_word": "Example",
    #     "reply": "Example",
    #     "only": "None"
    # }
    
    ## eh
    {
        "search_word": "shut up",
        "reply": "How about YOU shut up instead!?",
        "only": "None"
    },
    # {
    #     "search_word": "clanker",
    #     "reply": "You're the clanker.",
    #     "only": "None"
    # },

    ## Affection
    {
        "search_word": "belly rubs",
        "reply": ">w<",
        "only": "None"
    },
    
    {
        "search_word": "chin scratch",
        "reply": ">w<",
        "only": "None"
    },
    {
        "search_word": "ear scratch",
        "reply": ">w<",
        "only": "None"
    },
    {
        "search_word": "scratches chin",
        "reply": ">w<",
        "only": "None"
    },
    {
        "search_word": "scratches ears",
        "reply": ">w<",
        "only": "None"
    },

    {
        "search_word": "pat",
        "reply": ">w<",
        "only": "None"
    },
    {
        "search_word": "boop",
        "reply": ">w<",
        "only": "None"
    },
    {
        "search_word": "hug",
        "reply": "^w^",
        "only": "None"
    },
    {
        "search_word": "lick",
        "reply": ">/////<",
        "only": "None"
    },
    {
        "search_word": "kiss",
        "reply": ">/////<",
        "only": "proots and mother"
    },
    {
        "search_word": "mawh",
        "reply": ">/////<",
        "only": "proots and mother"
    }
]

class ShutUp(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if len(msg.mentions) < 1:
            return
        
        # 13/03/2026 - Bugfix: DMs can cause some issues.
        # if isinstance(msg.channel, discord.DMChannel):
        #     return
        

        for mention in msg.mentions:
            # If the mentioned user is the bot.
            if mention.id == self.bot.user.id:
                if SemiFunc.in_string(msg.content, 'clanker'):
                    await msg.reply("Do not call me that.")
                    await msg.delete()
                    return
                
                
                for response in responses:
                    users = get_users_config_entry(response['only'])

                    if SemiFunc.in_string(msg.content, response['search_word']):
                        can_send = True

                        if len(users) > 0:
                            if msg.author.id in users:
                                can_send = True
                            else:
                                can_send = False

                        if can_send:
                            await msg.reply(response['reply'])

async def setup(bot):
    await bot.add_cog(ShutUp(bot))