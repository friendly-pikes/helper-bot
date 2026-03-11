import re
import discord

from datetime import datetime
from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc
from utils.files import files
from misc import banished_words_private as banished_words_privateA

class OnMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        doLog = True
        
        # If main server, set doLog to config's log_audits_enabled value
        if message.guild.id == 1414222707570118656:
            doLog = files.get_config_entry("log_audits_enabled")
        

        if doLog:
            if message.author.bot == False:
                shouldLog = True
                
                banished = SemiFunc.banished_words
                banished_words_noignore = SemiFunc.banished_words_noignore
                banished_words_private = banished_words_privateA.private_banished()
                msg_content_lower = message.content.lower()
                content_lower_final = re.sub(r'[(#@-_\\/^,.)]', '', msg_content_lower).replace(" ", "")

                for banished_thing in banished:
                    if msg_content_lower.find(banished_thing) >= 0:
                        shouldLog = False
                            
                            
                # Last now - Private banish word list
                for banished_thing in banished_words_private:
                    if msg_content_lower.find(banished_thing) >= 0:
                        shouldLog = False
                
                # These are banished for ALL, even staff.
                for banished_thing in banished_words_noignore:
                    if content_lower_final.find(banished_thing) >= 0:
                        shouldLog = False
                

                if shouldLog:
                    # if SemiFunc.is_banished_word(message) == False:
                    auditChannelId = files.get_channel_id(message, "audit")
                    auditChannel = self.bot.get_channel(auditChannelId)
                            
                    embed = self.bot.create_embed_notitle(
                        description=f"**Message sent by {message.author.mention} was deleted in {message.channel.mention}**",
                        color=discord.Color.red(),
                        fields=[
                            {
                                "name": "message:",
                                "value": f"```{message.content}```",
                                "inline": False
                            },
                        ]
                    )

                    embed.timestamp = datetime.utcnow()
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar)
                    embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")
                            
                    await auditChannel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnMessageDelete(bot))
