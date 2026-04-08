import discord

from datetime import datetime
from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files

class OnMessageEdit(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if not isinstance(before.channel, discord.DMChannel):
            doLog = True
            
            # If main server, set doLog to config's log_audits_enabled value
            
            if not before.author.bot:
                if before.guild.id == 1414222707570118656:
                    doLog = files.get_config_entry("log_audits_enabled")
                    
                if doLog:
                    if before.author.bot == False:
                        # Makes sure the message is ACTUALLY edited.
                        if before.content != after.content:
                            auditChannelId = files.get_channel_id(before, "audit")
                            auditChannel = self.bot.get_channel(auditChannelId)
                            
                            follow = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"

                            embed = self.bot.create_embed_notitle(
                                description=f"**Message sent by {before.author.mention} was edited in {before.channel.mention}** [Jump To Message]({follow})",
                                color=discord.Color.blue(),
                                fields=[
                                    {
                                        "name": "before:",
                                        "value": f"```{before.content}```",
                                        "inline": False
                                    },
                                    {
                                        "name": "after:",
                                        "value": f"```{after.content}```",
                                        "inline": False
                                    }
                                ]
                            )

                            embed.timestamp = datetime.utcnow()
                            embed.set_author(name=before.author.name, icon_url=before.author.avatar)
                            embed.set_footer(text=f"Author: {before.author.id} | Message ID: {before.id}")
                            
                            await auditChannel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OnMessageEdit(bot))
