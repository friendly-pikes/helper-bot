from discord.ext import commands
from utils.discordbot import Bot
from utils.database import Database
from utils.semifunc import SemiFunc

class CreadyDatabases(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        Database.create_databases(self.bot.logger)
        # Database.create_database(self.bot.logger, "afk", [{"table_name": "users", "table_values": "(name TEXT, user_id INTEGER, msg TEXT, since TEXT)"}])


        # Update the banished list
        SemiFunc.update_banished(self.bot.logger)

        # Update the AFK users list
        SemiFunc.update_afk(self.bot.logger)

async def setup(bot):
    await bot.add_cog(CreadyDatabases(bot))
