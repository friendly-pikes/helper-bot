import discord

from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class OnMemberUpdated(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        if not before.bot:
            verifiedid = SemiFunc.get_role_id(before, "verified")
            welcome_ping = SemiFunc.get_role_id(before, "welcome_ping")
            gen_chat = after.guild.get_channel( SemiFunc.get_channel_id(before, "general-chat") )

            # Welcome message
            if before.get_role(verifiedid) == None and after.get_role(verifiedid):
                await gen_chat.send(f"<@&{welcome_ping}>\nWelcome {after.mention} to **{after.guild.name}**\nGet roles in <#1418954294656499773>\n\nWe hope you'll have a wonderful stay here!")
                # User @snowy 2.0 left from ー〔friendly pikes〕ー
                # hope you had a wonderful stay sorry that you had to leave

            # Timeout
            # if before.timed_out_until or after.timed_out_until:
            #     before_timeout = before.timed_out_until
            #     after_timeout = after.timed_out_until
            #     print(f"before: {before_timeout.time()}\nafter: {after_timeout.time()}\n")
            #     if before_timeout is not None and after_timeout is None:
            #         print(f"{before.name} timeout has expired")
        
        
async def setup(bot):
    await bot.add_cog(OnMemberUpdated(bot))
