import discord
import re

from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

dyno_ids = [
    1477499221577039923,
    1481064908391976990,
    155149108183695360
]

class DeleteBotMessages(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            if len(msg.embeds) > 0:
                for embed in msg.embeds:
                    # Dyno
                    if msg.author.id in dyno_ids:
                        # Delete Dyno's disabled command message, if it was sent
                        if embed.description.find("command is disabled in this server.") >= 0:
                            await msg.delete()

                        em_description = re.sub(r"[<#@0-9>*]", '', embed.description).replace(" ", "")

                        if str(em_description).find("MessagesentbyDeletedin") >= 0:
                            em_description = str(em_description).replace("MessagesentbyDeletedin\n", "")
                            banished = SemiFunc.banished_words
                            banished_words_noignore = SemiFunc.banished_words_noignore
                            # banished_words_private = banished_words_privateA.private_banished()
                            msg_content_lower = str(em_description).lower()
                            content_lower_final = re.sub(r'[(#@-_\\/^,.)]', '', msg_content_lower).replace(" ", "")
                            
                            shouldDelete = False

                            for banished_thing in banished:
                                if msg_content_lower.find(banished_thing) >= 0:
                                    shouldDelete = True
                                        
                            # Last now - Private banish word list
                            # for banished_thing in banished_words_private:
                            #     if msg_content_lower.find(banished_thing) >= 0:
                            #         shouldDelete = True
                            
                            # These are banished for ALL, even staff.
                            for banished_thing in banished_words_noignore:
                                if content_lower_final.find(banished_thing) >= 0:
                                    shouldDelete = True
                            
                            if shouldDelete:
                                await msg.delete()

                    ## Our bot
                    # elif msg.author.id == 1477564008772014142:
                    #     if len(msg.embeds) > 0:
                    #         embed:discord.Embed = msg.embeds[0]
                    #         should_del = False
                    #         if embed.description.find("was deleted in") >= 2:
                    #             for banished_thing in banished:
                    #                 if embed.description.find(banished_thing) >= 0:
                    #                     should_del = True
                    #             for banished_thing in banished_words_noignore:
                    #                 if embed.description.find(banished_thing) >= 0:
                    #                     should_del = True
                    #             if len(banished_words_private) > 0:
                    #                 for banished_thing in banished_words_private:
                    #                     if embed.description.find(banished_thing) >= 0:
                    #                         should_del = True

                    #         if should_del:
                    #             # print(f"\n{embed.title}\n{embed.description}")
                    #             await msg.delete()
            return
        

async def setup(bot):
    await bot.add_cog(DeleteBotMessages(bot))
