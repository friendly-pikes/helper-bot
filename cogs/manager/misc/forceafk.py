import discord

from utils.database import Database
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

# async def afk_cmd(self, ctx: Context, message: str, return_message: bool):
def usernick(guild: discord.Guild, user: discord.Member):
    nick = user.display_name
    errors = []
        
    if user.nick != nick:
        if user.nick == None:
            nick = user.display_name
        else:
            nick = user.nick
    
    # 22/03/2026 - Prevent AFK status "stacking"
    if nick.find("[AFK]") >= 0:
        # print("they has afk in nick")
        nick = nick.replace("[AFK] ", "")
    # print(nick)

    # Discord's nickname character limit is 32.
    if len(nick) > 26:
        # errors.append("I cannot put 'AFK' in your nickname because of character limits (32 max.)")
        errors.append("I cannot put 'AFK' in their nickname because of the nickname character limit. (32 max.)")
    
    # We can't change the server owner's nick.
    if user.id == guild.owner_id:
        errors.append("I cannot change their nickname.")

    return {"nick": nick, "errors": errors}

class ManagerCommands__Misc__ForceAFK(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="forceafk")
    async def forceafk(self, ctx: Context, id: str, *, message: str):
        """
        Forcefully add a user afk status.. works if they don't have a afk status already

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        id: str
            The id of the user
        message: str
            The message you want to use
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
            
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            if SemiFunc.is_command_exception(ctx.author, "reload"):
                pass
            else:
                await ctx.reply("That command is only usable by owners and managers.")
                return
        
        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        is_already_afk = False

        for user in SemiFunc.afk_users:
            if user['user_id'] == int(id):
                is_already_afk = True

        user = ctx.guild.get_member(int(id))

        if is_already_afk:
            await ctx.reply("Cannot change their status to AFK because they've already used ?afk or /afk.")
        else:
            cursor = Database.userdata_conn.cursor()
            
            nick = usernick(ctx.guild, user)
            afkSince_createdat = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")

            cursor.execute(f'INSERT INTO afk_users VALUES ({user.id}, "{nick['nick']}", "{message}", "{afkSince_createdat}", 0)')

            Database.userdata_conn.commit()

            try:
                if len(nick['nick']) > 26:
                    msg = f"I've set their status to AFK with the message `{message}`"
                    if len(nick['errors']) > 0:
                        msg = f"{msg}\n..however:"

                    for error in nick['errors']:
                        msg = f"{msg}\n{error}"
                    await ctx.reply(msg)
                else:
                    await user.edit(nick=f"[AFK] {nick['nick']}")
                    await ctx.reply(f"I've set their status to AFK with the message `{message}`")
            except Forbidden as e:
                if e.text == "Missing Permissions":
                    await ctx.reply(f"I've set their status to AFK with the message `{message}`\n..however I cannot change their nickname to show their're AFK.")
            # except CommandInvokeError as e:
            #     print(e)

            # Update the AFK users list
            SemiFunc.update_afk(self.bot.logger)
        
        


async def setup(bot):
    await bot.add_cog(ManagerCommands__Misc__ForceAFK(bot))
