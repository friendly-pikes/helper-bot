###############################################
#
# File: listeners.on__ready.database
# Date: 09/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################



from discord.ext import commands
from utils.discordbot import Bot
from utils.database import Database

class OnReadyDatabase(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # 21/03/2026 - Changed so we get all servers instead of just the main
        # .. for other reasons (one is that testing outside of snowy's system)
        for guild in self.bot.guilds:
            # Fuck my fluffy life.. getting members from create_databases didn't work, on_ready it is...
            for member in guild.members:
                if member.bot == False:
                    user = Database.userdata_conn.execute(f'SELECT * FROM user_data WHERE user_id={member.id}')
                    if len(user.fetchall()) < 1:
                        Database.userdata_conn.execute(f'INSERT INTO user_data VALUES (0, {member.id}, "{member.name}", "NULL", 0, 0, 0)')
                    else:
                        data = Database.userdata_conn.execute(f'SELECT * FROM user_data WHERE user_id={member.id}').fetchone()
                        if data != None:
                            user_name = data[2]

                            if member.name != user_name:
                                Database.userdata_conn.execute(f"UPDATE user_data SET alise=? WHERE user_id=?", (member.name, member.id))
                                # Database.userdata_conn.commit()
            Database.userdata_conn.commit()

        print("Added all users to database.")
        

async def setup(bot):
    await bot.add_cog(OnReadyDatabase(bot))
