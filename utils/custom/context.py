###############################################
#
# File: utils.custom.context
# Date: 01/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################



from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.discordbot import Bot


class Context(commands.Context):
    """
    This class is used to overwrite discord.py's Context class.
    You can add your own methods here.
    Any functions you add will automatically become usable in ALL commands.

    Example:
    --------
    def ping(self) -> str:
        return "Hello world!"

    @commands.hybrid_command()
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong! {ctx.ping()}")
    """
    def __init__(self, **kwargs):
        self.bot: "Bot"
        super().__init__(**kwargs)
