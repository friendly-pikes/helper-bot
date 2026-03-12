
import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import SemiFunc

class JoinMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = member.guild.get_channel( SemiFunc.get_channel_id(member, "welcome") )

        if files.get_config_entry("join_message_enabled"):
            await welcome_channel.send(f"Hello {member.mention}! Welcome to the server! :3")

async def setup(bot):
    await bot.add_cog(JoinMessage(bot))
