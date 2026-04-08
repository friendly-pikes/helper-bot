import sqlite3

from utils.database import Database
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

# async def afk_cmd(self, ctx: Context, message: str, return_message: bool):
def usernick(ctx: Context):
    nick = ctx.author.display_name
    errors = []
        
    if ctx.author.nick != nick:
        if ctx.author.nick == None:
            nick = ctx.author.display_name
        else:
            nick = ctx.author.nick
    
    # 22/03/2026 - Prevent AFK status "stacking"
    if nick.find("[AFK]") >= 0:
        # print("they has afk in nick")
        nick = nick.replace("[AFK] ", "")
    # print(nick)

    # Discord's nickname character limit is 32.
    if len(nick) > 26:
        # errors.append("I cannot put 'AFK' in your nickname because of character limits (32 max.)")
        errors.append("I cannot put 'AFK' in your nickname because of the nickname character limit. (32 max.)")
    
    # We can't change the server owner's nick.
    if ctx.author.id == ctx.guild.owner_id:
        errors.append("I cannot change your nickname.")

    return {"nick": nick, "errors": errors}

class UserCommands__Misc__AFK(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    ## Values for database table:
    # 0 - user_id
    # 1 - nickname
    # 2 - message
    # 3 - afk_since
    # 4 - toggle

    @commands.guild_only()
    @commands.hybrid_command(name="afk")
    async def afk(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        """
        Set your status to AFK

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        message: str
            The message you want to use
        return_message: str
            Toggle the return message (UNUSED)
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        # if SemiFunc.is_command_exception(ctx.author, "afk") or SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await afk_cmd(self, ctx, message, return_message)
        #     return
            
        # if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await ctx.reply("That command is staff only.")
        #     return
        

        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        is_already_afk = False

        for user in SemiFunc.afk_users:
            if user['user_id'] == ctx.author.id:
                is_already_afk = True

        if is_already_afk:
            await ctx.reply("Cannot change your status to AFK because you've already used ?afk or /afk. Did you mean to use ?afkupdate?")
        else:
            cursor = Database.userdata_conn.cursor()
            
            nick = usernick(ctx)
            afkSince_createdat = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")

            cursor.execute(f'INSERT INTO afk_users VALUES ({ctx.author.id}, "{nick['nick']}", "{message}", "{afkSince_createdat}", 0)')

            Database.userdata_conn.commit()

            try:
                if len(nick['nick']) > 26:
                    msg = f"I've set your status to AFK with the message `{message}`"
                    if len(nick['errors']) > 0:
                        msg = f"{msg}\n..however:"

                    for error in nick['errors']:
                        msg = f"{msg}\n{error}"
                    await ctx.reply(msg)
                else:
                    await ctx.author.edit(nick=f"[AFK] {nick['nick']}")
                    await ctx.reply(f"I've set your status to AFK with the message `{message}`")
            except Forbidden as e:
                if e.text == "Missing Permissions":
                    await ctx.reply(f"I've set your status to AFK with the message `{message}`\n..however I cannot change your nickname to show you're AFK.")
            # except CommandInvokeError as e:
            #     print(e)

            # Update the AFK users list
            SemiFunc.update_afk(self.bot.logger)
        
        
    @commands.guild_only()
    @commands.hybrid_command(name="afkupdate")
    async def afkupdate(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        """
        Update your afk status

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        message: str
            The new afk message you want to use
        return_message: bool
            Toggle the return message (UNUSED)
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        # if SemiFunc.is_command_exception(ctx.author, "afk") or SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await afk_cmd(self, ctx, message, return_message)
        #     return
            
        # if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await ctx.reply("That command is staff only.")
        #     return


        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        is_already_afk = False

        for user in SemiFunc.afk_users:
            if user['user_id'] == ctx.author.id:
                is_already_afk = True

        if is_already_afk:
            cursor = Database.userdata_conn.cursor()

            cursor.execute(f"UPDATE afk_users SET message=? WHERE user_id = ?", (message, ctx.author.id))
            await ctx.reply(f"I've set your AFK message to `{message}`")

            Database.userdata_conn.commit()


            # Update the AFK users list
            SemiFunc.update_afk(self.bot.logger)
        else:
            await ctx.reply(f"Cannot set your AFK message because you've not used ?afk or /afk")

    @commands.guild_only()
    @commands.hybrid_command(name="afktoggle")
    async def afktoggle(self, ctx: Context):
        """
        Toggle your afk status from being removed from talking

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        # if SemiFunc.is_command_exception(ctx.author, "afk") or SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await afk_cmd(self, ctx, message, return_message)
        #     return
            
        # if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
        #     await ctx.reply("That command is staff only.")
        #     return


        await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
        
        is_already_afk = False

        for user in SemiFunc.afk_users:
            if user['user_id'] == ctx.author.id:
                is_already_afk = True

        if is_already_afk:
            cursor = Database.userdata_conn.cursor()
            toggle = cursor.execute(f"SELECT toggle FROM afk_users WHERE user_id = ?", (ctx.author.id,)).fetchone()[0]
            new_toggle = 1

            msg = "I've toggled your afk status from being removed.. it cannot be removed now from chatting."

            if toggle == 0:
                new_toggle = 1
                msg = "I've toggled your afk status from being removed.. it cannot be removed now from chatting."
            elif toggle == 1:
                new_toggle = 0
                msg = "I've toggled your afk status from being removed.. it can now be removed now from chatting."
            else:
                msg = "I've toggled your afk status from being removed.. it cannot be removed now from chatting."
                new_toggle = 1

            cursor.execute(f"UPDATE afk_users SET toggle=? WHERE user_id = ?", (new_toggle, ctx.author.id))
            await ctx.reply(msg)

            Database.userdata_conn.commit()


            # Update the AFK users list
            SemiFunc.update_afk(self.bot.logger)
        else:
            await ctx.reply(f"Cannot use afktoggle because you've not used ?afk or /afk")

async def setup(bot):
    await bot.add_cog(UserCommands__Misc__AFK(bot))
