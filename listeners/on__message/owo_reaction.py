import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.files import files
from utils.semifunc import SemiFunc

class OwOReaction(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        # 13/03/2026 - Bugfix: DMs can cause some issues.
        if not isinstance(msg.channel, discord.DMChannel):
            # OwO reaction
            if msg.content.lower() == "owo" or msg.content.lower() == "<:fox_owo:1479235584127143978>":
                # Do not owo react in audits
                if msg.channel.id != SemiFunc.get_channel_id(msg, "audit"):
                    owoId = files.get_emoji_ids(msg.guild.id)['owo']
                    owo = await msg.guild.fetch_emoji(owoId)
                    await msg.add_reaction(owo)
        

async def setup(bot):
    await bot.add_cog(OwOReaction(bot))
