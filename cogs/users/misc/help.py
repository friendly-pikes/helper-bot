# nah nvm fuck u

import sqlite3

from utils.database import Database
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class UserCommands__Misc__Help(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        
    # @commands.guild_only()
    # @commands.hybrid_command(name="help")
    # async def help(self, ctx: Context):
    #     """
    #     Update your afk status

    #     Parameters
    #     ----------
    #     ctx: Context
    #         The context of the command invocation
    #     message: str
    #         The new afk message you want to use
    #     return_message: bool
    #         Toggle the return message (UNUSED)
    #     """
    #     if SemiFunc.command_disabled(ctx):
    #         await ctx.reply("That command is currently disabled.")
    #         return
        
    #     if ctx.channel.id != SemiFunc.get_channel_id(ctx, 'bot-commands'):
    #         # we need to test.. ffs
    #         if ctx.channel.id != 1480563782030852212:
    #             # Use in bot commands you goober
    #             await ctx.reply("Use that command in <#1477493580061741156>")
    #             return

    #     cmds = {
    #         "UserCommands": {
    #             "name": "User (anyone can use these)",
    #             "cmds": [

    #             ]
    #         },
    #         "StaffCommands": {
    #             "name": "Staff (staff can use these)",
    #             "cmds": [
    #                 # {
    #                 #     "name": "whatever",
    #                 #     "description": "whatever",
    #                 #     "arguments": [
    #                 #         {
    #                 #             "name": "arg name",
    #                 #             "description": "arg description"
    #                 #         }
    #                 #     ]
    #                 # }
    #             ]
    #         },
    #         "ManagerCommands": {
    #             "name": "Manager (managers and owners can use these)",
    #             "cmds": [
                    
    #             ]
    #         }
    #     }
        
    #     # Add categories for the cog names
    #     for command in self.bot.commands:
    #         # "checking. It's the cool thing to do."
    #         if command.cog_name.startswith("UserCommands"):
    #             arguments = []
    #             if len(command.clean_params) > 0:
    #                 # print(f"{command.name} - {command.clean_params}")
    #                 for arg in command.clean_params:
    #                     arguments.append({
                            
    #                     })
    #                     # print(command.params)
    #                     print(command.params[arg].name)
    #                     print(command.params[arg].description)
    #                     print(command.params[arg].required)
    #                     print("\n")
    #                     # print(arg)

    #         #     cmds["UserCommands"][cmds].append({
    #         #         "name": command.name,
    #         #         "description": command.description
    #                 # "arguments": 
    #         #     })

    #         # if command.cog_name.startswith("StaffCommands"):
    #         #     if SemiFunc.can_use_command(ctx, ctx.author, "staff") == True:
                    
    #         # if command.cog_name.startswith("ManagerCommands"):
    #         #     if SemiFunc.can_use_command(ctx, ctx.author, "manager") == True:
    #         #         can_add = False
        
async def setup(bot):
    await bot.add_cog(UserCommands__Misc__Help(bot))
