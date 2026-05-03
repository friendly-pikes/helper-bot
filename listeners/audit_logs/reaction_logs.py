###############################################
#
# File: listeners.audit_logs.reaction_logs
# Date: 29/04/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord
from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc
from datetime import datetime

class ReactionLogs(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id == 1418954294656499773:
            return
        
        
        add_logs = self.bot.get_channel(1498875159874900119)
        remove_logs = self.bot.get_channel(1498876183847112885)
        if payload.member.bot == False:
            embed = self.bot.create_embed_notitle(color=discord.Color.red())
            message = f"https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}"
            
            embed.description = f"**Reaction added to {message}**"
            embed.add_field(name="emoji:",value=f"```{payload.emoji}```",inline=False)
            
            embed.timestamp = datetime.utcnow()
            if payload.member:
                embed.set_author(name=payload.member.name, icon_url=payload.member.avatar)
            embed.set_footer(text=f"Author: {payload.message_author_id} | Message ID: {payload.message_id}")

            await add_logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.channel_id == 1418954294656499773:
            return
        add_logs = self.bot.get_channel(1498875159874900119)
        remove_logs = self.bot.get_channel(1498876183847112885)

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        if member.bot == False:
            embed = self.bot.create_embed_notitle(color=discord.Color.red())
            message = f"https://discord.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}"
            
            embed.description = f"**Reaction removed from {message}**"
            embed.add_field(name="emoji:",value=f"```{payload.emoji}```",inline=False)
            
            embed.timestamp = datetime.utcnow()
            if member:
                embed.set_author(name=member.name, icon_url=member.avatar)
            embed.set_footer(text=f"Author: {payload.message_author_id} | Message ID: {payload.message_id}")

            await remove_logs.send(embed=embed)

        

async def setup(bot):
    await bot.add_cog(ReactionLogs(bot))
