import os
import random
import dotenv
import asyncio
import discord
import threading
import web.app as app

from web.app import run as run_web
from datetime import datetime

good_to_go = True

### Removed as I now include my misc file.. only check that was kept is the env file cuz you need the bot token.
# Check if the stuff we need exist first before trying shit
# if not os.path.exists('misc'):
#     good_to_go = False
#     print('You need the "misc" folder! Copy "misc_example" and rename it to "misc".\n..or rename "misc_example" to "misc".')
if not os.path.exists('.env'):
    good_to_go = False
    print('You need a ".env" file! Copy ".env.example" and rename it to ".env".\n..or rename ".env.example" to ".env".')


if good_to_go == True:
    # "Good to go!" - Robin Atkin Downes / TF2 Medic Voice Actor
    
    import utils.files as files
    from utils.discordbot import Bot
    dotenv.load_dotenv()

    token = os.getenv('DISCORD_TOKEN')
    config = files._config()

    bot = Bot(
        command_prefix=config['prefix'],
        prefix=config['prefix'], command_attrs=dict(hidden=True),
        allowed_mentions=discord.AllowedMentions(
            everyone=False, roles=True, users=True
        ),
        intents=discord.Intents.all(),
        help_command = None,
        case_insensitive=True
    )

    app.bot_instance = bot
    
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

    try:
        bot.run(token)

    except Exception as e:
        bot.logger.error(f"Error when logging in: {e}")
