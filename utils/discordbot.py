import os
import json
import random
import asyncio
import discord
import datetime
import logging
import logging.handlers

from utils.custom.context import Context
# from utils import permissions
import utils.files as files
from discord.ext.commands import AutoShardedBot, DefaultHelpCommand

class Bot(AutoShardedBot):
    def __init__(self, prefix: str = "!", *args, **kargs):
        super().__init__(*args, **kargs)
        
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
            filename=f"./logs/{datetime.datetime.now().strftime('%d-%m-%Y %H-%M')}.log",
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger
        self.shutting_down = False
        # self.get_all_emojis() = self.emojis
    
    async def close(self):
        if self.is_ready() == True:
            print("im dying")

            self.shutting_down = True

            await asyncio.sleep(0.1)
            # test_server = self.get_guild(1480087423433052242)
            # status_channel = test_server.get_channel(1482618083263643698)

            # status_message = await status_channel.fetch_message(1482633940039630869)
            
            # if self.user.id == 1482861019582693507:
            #     status_message = await status_channel.fetch_message(1483989253045358602)

            # if status_message != None:
            #     # uname = platform.uname()
            #     # svmem = psutil.virtual_memory()
            #     # node_name = uname.node

            #     # bot_drive = None
            #     # bot_drive_usage = None
            #     # for i, part in enumerate(psutil.disk_partitions()):
            #     #     if part.mountpoint.startswith("D"):
            #     #         bot_drive = part
            #     #         bot_drive_usage = psutil.disk_usage(part.mountpoint)

            #     embed = self.create_embed(
            #         # 🖥️ {node_name} | STATUS
            #         f"🖥️ {self.user.display_name} | STATUS",
            #         description="Updates every minute.\n\n",
            #         color=discord.Color.red(),
            #         fields=[
            #             {
            #                 "name": "🔴 Status",
            #                 "value": "Offline",
            #                 "inline": True
            #             }
            #             # {
            #             #     "name": "📊 Current Metrics",
            #             #     "value": f"• CPU: {psutil.cpu_percent()}%\n• Memory: {get_size(svmem.used)} / {get_size(svmem.available)} ({svmem.percent}%)",
            #             #     "inline": False
            #             # },
            #             # {
            #             #     "name": "Extra",
            #             #     "value": f"• SSD: {get_size(bot_drive_usage.used)} / {get_size(bot_drive_usage.total)} ({bot_drive_usage.percent}%)",
            #             #     "inline": False
            #             # }
            #         ]
            #     )

            #     embed.set_footer(text=f"Last updated: {datetime.datetime.now().strftime('%d/%m/%Y, %H:%M')}")
            #     embed.timestamp = datetime.datetime.utcnow()

            #     await status_message.edit(
            #         embed=embed
            #     )
            #     embed.set_footer(text=f"Last updated: {datetime.datetime.now().strftime('%d/%m/%Y, %H:%M')}")
            #     embed.timestamp = datetime.datetime.utcnow()

            #     await status_message.edit(content="",embed=embed)
            print("XwX")

            await super().close()
        
    # def create_embed_notitle(self, title:str = "Embed Title", description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: [] = []):
    def create_embed_notitle(self, description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: list = [], use_by_snow2code_footer: bool = False):
        embed = discord.Embed(description=description, color=color)
        
        if len(fields) > 0:
            for field in fields:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

        if use_by_snow2code_footer:
            embed.set_footer(text="Bot developed by snow2code")

        return embed
    
    def create_embed(self, title:str = "Embed Title", description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: list = [], use_by_snow2code_footer: bool = False):
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
                for sub in os.listdir(f"cogs/{who}"):
                    if sub != "__pycache__":
                        if sub.endswith(".py"):
                            commands = commands + 1
                            name = sub[:-3]
                            await self.load_extension(f"cogs.{who}.{name}")
                        else:
                            for file in os.listdir(f"cogs/{who}/{sub}"):
                                # Ignore files that aren't .py files
                                if not file.endswith(".py"):
                                    continue
                                
                                commands = commands + 1
                                name = file[:-3]
                                await self.load_extension(f"cogs.{who}.{sub}.{name}")
        
        print(f"Loaded {commands} command files.\nLoaded {listeners} listener files.")
    
    async def process_commands(self, msg: discord.Message):
        ctx = await self.get_context(msg, cls=Context)
        
        if msg.content.lower().find("&topic") == 0:
            with open(files.get_filepath("commands", "json"), "r", encoding="utf8") as file:
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
