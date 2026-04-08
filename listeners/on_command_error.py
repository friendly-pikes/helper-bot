import os

from datetime import datetime
from discord.ext import commands
from utils.discordbot import Bot
from utils.custom.context import Context

class OnCommandError(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        # 13/03/2026 - Send certain messages depending on the error.
        err_handled_already = False

        if isinstance(error, commands.NoPrivateMessage):
            err_handled_already = True
            await ctx.reply("The commands are only usable in a server!")
        elif isinstance(error, commands.BadArgument):
            err_handled_already = True
            await ctx.reply("A argument for that command is bad... give it another go.?")
        elif isinstance(error, commands.MissingRequiredArgument):
            err_handled_already = True
            await ctx.reply("You *might* be missing a argument for that command.. or something has gone terribly wrong.")


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

            # 14/03/2026 - mute error:
            if ctx.command.name == "mute":
                await ctx.reply(f"Argument missing or invaild duration. Duration Examples:\n5s-5 seconds\n5m-5 minutes\n5h-5 hours\n5d- 5 days\n\nMax duration is 28 days.")
            else:
                if err_handled_already == False:
                    await ctx.reply(f"An error occured with the command! {mention_snowy}\n\n```{error}```")
                    self.bot.logger.warn(f"An error occured with the command '{command_name}' used by {ctx.author.name}!\n{error}\n")

            if err_handled_already == False:
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
