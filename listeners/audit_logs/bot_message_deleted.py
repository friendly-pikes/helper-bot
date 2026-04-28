import discord

from datetime import datetime
from discord.ext import commands
from utils.discordbot import Bot

class OnBotMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if not isinstance(message.channel, discord.DMChannel):
            if message.author.id == self.bot.user.id:

                if message.embeds == None or len(message.embeds) < 1:
                    private_logs = self.bot.get_channel(1485986725728882789)

                    if private_logs:
                        embed = self.bot.create_embed_notitle(color=discord.Color.red())

                        embed.description = f"**Message sent by {message.author.mention} was deleted in {message.channel.mention}**"
                        embed.add_field(name="message:",value=f"```{message.content}```",inline=False)

                        embed.timestamp = datetime.utcnow()
                        embed.set_author(name=message.author.name, icon_url=message.author.avatar)
                        embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")


                        await private_logs.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OnBotMessageDelete(bot))