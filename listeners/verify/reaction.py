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
        if payload.member.bot == False:
            ## Stupid raw thing, so we gotta.. yea
            if payload.channel_id == SemiFunc.get_channel_id(payload.member, "verify"):
                if payload.emoji.name == "✅":
                    id = SemiFunc.get_role_id(payload.member, "verified")
                    verified = payload.member.guild.get_role(id)
                    await payload.member.add_roles(verified)
        

async def setup(bot):
    await bot.add_cog(VerifyReaction(bot))
