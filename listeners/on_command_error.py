import os
import discord
from datetime import datetime
from discord.ext import commands
from utils.discordbot import Bot
from utils.custom.context import Context
from utils.semifunc import SemiFunc

class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        # 13/03/2026 - Send certain messages depending on the error.
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.reply("The commands are only usable in a server!")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("You're missing a argument for that command.")


        if not os.path.exists("logs/errors"):
            os.makedirs("logs/errors")
        if not os.path.exists("logs/errors/commands"):
            os.makedirs("logs/errors/commands")

        if ctx.command:
            # if ctx.command.name in ["reply", "repeat"]:
            #     await ctx.message.delete()
            #     return
            
            mention_snowy = "<@888072934114074624>"
            command_name = ctx.command.name
            date = datetime.now().strftime('%d-%m-%Y at %H-%M-%S')

            # if ctx.interaction != None:
            #     command_name = ctx.interaction.command.name

            await ctx.reply(f"An error occured with the command! {mention_snowy}\n\n```{error}```")
            self.bot.logger.warn(f"An error occured with the command '{command_name}' used by {ctx.author.name}!\n{error}\n")

            with open(f"logs/errors/commands/{date}", "w") as f:
                f.write(f"An error occured with {ctx.command.name} ran by {ctx.author.name} on {date}\n\nError: {error}")
        else:
            date = datetime.now().strftime('%d-%m-%Y at %H-%M-%S')
            if str(error).find("is not found") >= 0:
                cmd = str(error).lower()
                cmd = cmd.replace('"', "")
                cmd = cmd.replace(' ', "")
                cmd = cmd.replace("isnotfound", "")
                cmd = cmd.replace("command", "")

                if cmd.find("?") < 0:
                    self.bot.logger.warn(f"An error occured!\n{error}\n")
                    with open(f"logs/errors/{date}", "w") as f:
                        f.write(f"An error occured on {date}\n\nError: {error}")
            else:
                with open(f"logs/errors/{date}", "w") as f:
                    f.write(f"An error occured on {date}\n\nError: {error}")
                self.bot.logger.warn(f"An error occured!\n{error}\n")
        
async def setup(bot):
    await bot.add_cog(OnCommandError(bot))
