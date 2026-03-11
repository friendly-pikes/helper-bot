import os
import json
import random
import discord
import datetime
import logging
import logging.handlers

from utils.custom.context import Context
# from utils import permissions
import utils.files as files
from discord import app_commands
from discord.ext.commands import AutoShardedBot, DefaultHelpCommand


class Bot(AutoShardedBot):
    def __init__(self, prefix: str = "!", *args, **kargs):
        super().__init__(*args, **kargs)
        
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
            filename=f"./misc/logs/{datetime.datetime.now().strftime('%d-%m-%Y %H-%M')}.log",
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger
        # self.get_all_emojis() = self.emojis
        
    # def create_embed_notitle(self, title:str = "Embed Title", description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: [] = []):
    def create_embed_notitle(self, description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: [] = [], use_by_snow2code_footer: bool = False):
        embed = discord.Embed(description=description, color=color)
        
        if len(fields) > 0:
            for field in fields:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

        if use_by_snow2code_footer:
            embed.set_footer(text="Bot developed by snow2code")

        return embed
    
    def create_embed(self, title:str = "Embed Title", description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: [] = [], use_by_snow2code_footer: bool = False):
        embed = discord.Embed(title=title, description=description, color=color)
        
        if len(fields) > 0:
            for field in fields:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

        if use_by_snow2code_footer:
            embed.set_footer(text="Bot developed by snow2code")
        
        return embed

    async def setup_hook(self):
        ## Load listener cogs
        listeners = 0
        commands = 0
        for what in os.listdir("listeners"):
            gud = True
            if what == "__pycache__":
                gud = False
            else:
                if what.endswith(".py"):
                    gud = False
                    listeners = listeners + 1
                    name = what[:-3]
                    await self.load_extension(f"listeners.{name}")

            if gud:
                for file in os.listdir(f"listeners/{what}"):
                    # Ignore files that aren't .py files
                    if not file.endswith(".py"):
                        continue

                    listeners = listeners + 1
                    name = file[:-3]
                    await self.load_extension(f"listeners.{what}.{name}")
            
        ## Load command cogs
        for who in os.listdir("cogs"):
            gud = True
            if who == "__pycache__":
                gud = False

            if gud:
                for file in os.listdir(f"cogs/{who}"):
                    # Ignore files that aren't .py files
                    if not file.endswith(".py"):
                        continue
                    
                    commands = commands + 1
                    name = file[:-3]
                    await self.load_extension(f"cogs.{who}.{name}")
        
        print(f"Loaded {commands} command files.\nLoaded {listeners} listener files.")
    
    async def process_commands(self, msg: discord.Message):
        ctx = await self.get_context(msg, cls=Context)
        
        if "topic" in msg.content:
            if msg.content == "&topic":
                topics = None
                topic = ""
                commands = files.get_filepath("commands", "json")

                with open(commands, "r", encoding="utf8") as file:
                    data = json.load(file)
                    topics = data['topics']
                

                topic = random.choice(topics)

                await ctx.send(f"{topic}?")
        else:
            await self.invoke(ctx)

# class HelpFormat(DefaultHelpCommand):
#     def get_destination(self, no_pm: bool = False):
#         if no_pm:
#             return self.context.channel
#         else:
#             return self.context.author

#     async def send_error_message(self, error: str) -> None:
#         """ Sends an error message to the destination. """
#         destination = self.get_destination(no_pm=True)
#         await destination.send(error)

#     async def send_command_help(self, command) -> None:
#         """ Sends the help for a single command. """
#         self.add_command_formatting(command)
#         self.paginator.close_page()
#         await self.send_pages(no_pm=True)

#     async def send_pages(self, no_pm: bool = False) -> None:
#         """ Sends the help pages to the destination. """
#         try:
#             if permissions.can_handle(self.context, "add_reactions"):
#                 await self.context.message.add_reaction(chr(0x2709))
#         except discord.Forbidden:
#             pass

#         try:
#             destination = self.get_destination(no_pm=no_pm)
#             for page in self.paginator.pages:
#                 await destination.send(page)
#         except discord.Forbidden:
#             destination = self.get_destination(no_pm=True)
#             await destination.send("Couldn't send help to you due to blocked DMs...")
