import discord

from logging import Logger
from datetime import datetime
from utils.custom.context import Context
from utils.database import Database
import utils.files as files

class Economy():
    def __init__(*args, **kargs):
        super().__init__(*args, **kargs)

    def econ_embed(title: str="Title", description: str="Description", user: discord.Member=None, fields: [] = []):
        embed = discord.Embed(title=title,description=description,color=discord.Color.pink())

        if len(fields) > 0:
            for field in fields:
                embed.add_field(name=field['name'],value=field['value'],inline=field['inline'])

        embed.set_footer(text="Bot developed by snow2code")
        if user != None:
            embed.set_author(name=user.name, icon_url=user.avatar)

        return embed

    def get_curreny_name():
        return files.get_config_entry("currency_name")
        
    def format_amount(amount: int):
        amount = round(amount, 2)
        return f'{amount:,}'

    def use_econ(ctx: Context, user: discord.Member, logger: Logger):
        conn = Database.userdata_conn.cursor()

        conn.execute(f'UPDATE user_data SET used=? WHERE user_id=?', (1, ctx.author.id))


    def econ__is_on_cooldown(ctx: Context, user: discord.Member, logger: Logger):
        cooldowns = Database.userdata_conn.cursor().execute("SELECT * FROM cooldowns")
        usr_cooldown = None

        for cooldown in cooldowns:
            if cooldown[0] == user.id and cooldown[1] == ctx.command.name:
                usr_cooldown = cooldown

        if usr_cooldown != None:
            date_cooldown = usr_cooldown[2]
            date_now = datetime.now().strftime('%d/%m/%Y')

            day_cooldown = int(date_cooldown[:2])
            day_now = int(date_now[:2])
                
            #  Snowy:
            # Confused me a bit. so-
            # If the current day is more than the cooldowns day, return False.
            if day_now > day_cooldown:
                Database.userdata_conn.cursor().execute(f'DELETE FROM cooldowns WHERE user_id={user.id} AND command="{ctx.command.name}"')
                Database.userdata_conn.commit()

                logger.info(f"Removed {user.name}'s cooldown.")

                return False
            return True
        return False

    def econ__put_on_cooldown(ctx: Context, user: discord.Member, logger: Logger):
        date = datetime.now().strftime('%d/%m/%Y')
        if Economy.econ__is_on_cooldown(ctx, user, logger) == False:
            Database.userdata_conn.cursor().execute(f'INSERT INTO cooldowns VALUES ({user.id}, "{ctx.command.name}", "{date}")')
            Database.userdata_conn.commit()
            
            logger.info(f"Put {user.name} on a cooldown for {ctx.command.name}.")