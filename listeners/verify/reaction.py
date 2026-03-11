from discord import *
from discord.ext import commands
from utils.discordbot import Bot
from utils.custom.context import Context
from utils.semifunc import SemiFunc

class VerifyReaction(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        verify_channel_id = await self.bot.fetch_channel(payload.channel_id)
        if payload.member.bot == False:
            if payload.channel_id == verify_channel_id:
                # self.bot.get_channel(payload.channel_id)
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                print(msg)
        

async def setup(bot):
    await bot.add_cog(VerifyReaction(bot))
