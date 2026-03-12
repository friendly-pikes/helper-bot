import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import SemiFunc

class DammyFiles(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        banished_ids = SemiFunc.banished_ids

        if member.id in banished_ids:
            role = member.guild.get_role( SemiFunc.get_role_id(member, "banished") )
            channel = member.guild.get_channel( SemiFunc.get_channel_id(member, "audit") )
            
            embed = self.bot.create_embed(
                title="Dammy Files Banisher",
                description=f"User {member.display_name} ({member.name}) was banished. Reason being they are in the Dammy Files.\n\nUser Info:\nUser - {member.name}\nUserID - {member.id}",
                color=discord.Color.pink()
            )

            await member.add_roles(role)
            await channel.send(embed=embed)
            return

async def setup(bot):
    await bot.add_cog(DammyFiles(bot))
