import random
import asyncio

from discord import errors
from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc
import utils.files as files

async def status_loop(bot: Bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        # Every 16 minutes
        # 26/03/2026.. no, 20 minutes-
        await asyncio.sleep(1200)


        ## 26/03/2026
        # coffee:
        #  Random messages and numbers.
        #  like 67 (cuz why not.. this one was by me-),
        # beep, boop, blep, mlem, "What to do, what to do.. try and steal the ram on top of the fridge it is."

        # First a random message, then fox owo
        random_messages = files.get_bot_config_entry("random_messages")
        random_message = random.choice(random_messages)

        ## CONFIGURATION NEEDED HERE FOR WHO ISN'T SNOWY-
        general_chat = bot.get_channel(1414222708324958385)
        reaction = bot.get_emoji(1479235584127143978)
        should_send = True
        
        # test channel
        if bot.user.id == 1482861019582693507:
            general_chat = bot.get_channel(1486657608570900510)
            reaction = bot.get_emoji(1480095058811424842)
        
        # If the last message is by the bot, do not do shit
        if general_chat.last_message:
            if general_chat.last_message.author.id == bot.user.id:
                if SemiFunc.in_string(general_chat.last_message.content, "fox_owo") == False:
                    should_send = False

        if general_chat != None:
            if should_send:
                try:
                    await general_chat.send(random_message)
                except errors.HTTPException as e:
                    bot.logger.warn(f"listeners.bot_reactions.random_message - Got HTTPException. Message: {e}")
        else:
            bot.logger.warn("listeners.bot_reactions.random_messages - general_chat is None!! Edit the channel id you goober!")

        # owo?
        rand = random.randint(1, 100)

        if rand > 80:
            # If general_chat is none, don't send.. assume we are testing -w-
            if general_chat != None:
                if should_send:
                    await general_chat.send(content=f"<:{reaction.name}:{reaction.id}>")

class RandomMessages(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.owo = False

    @commands.Cog.listener()
    async def on_connect(self):
        if self.owo == False:
            self.owo = True
            # await change_status(self.bot)
            self.bot.loop.create_task(status_loop(self.bot))
            # await self.bot.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name="It's normal to lose interest in life.. snowy has lost *ALL* interest in life..."))

async def setup(bot):
    await bot.add_cog(RandomMessages(bot))
