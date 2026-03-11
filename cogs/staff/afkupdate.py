import sqlite3

from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

async def afk_cmd(self, ctx: Context, message: str, return_message: bool):
    await SemiFunc.log_command_use(self.bot, ctx.author, ctx.message.content, ctx.interaction, ctx)
    
    is_already_afk = False

    for user in SemiFunc.afk_users:
        if user['user_id'] == ctx.author.id:
            is_already_afk = True

    if is_already_afk:
        conn = sqlite3.connect(f"misc/afk.db")
        cursor = conn.cursor()

        cursor.execute(f"UPDATE users SET message=?, return_message=? WHERE user_id = ?", (message, return_message, ctx.author.id))

        conn.commit()
        conn.close()

    else:
        await ctx.reply(f"Cannot set your AFK message because you've not used ?afk or /afk")
        # conn = sqlite3.connect(f"misc/afk.db")
        # cursor = conn.cursor()
        
        # nick = ctx.author.display_name
        # afkSince_createdat = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")

        # if ctx.author.nick != nick:
        #     nick = ctx.author.nick

        # cursor.execute(f"INSERT INTO users VALUES ({nick}, {ctx.author.id}, {return_message}, {message}, {afkSince_createdat})")
        # conn.close()
        # # if is_already_afk:
        # #     
        # # else:
        # #     await ctx.reply(f"Cannot set your AFK message because you've not used ?afk or /afk")

        # try:
        #     await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
            
        # except Forbidden as e:
        #     if e.text == "Missing Permissions":
        #         await ctx.reply(f"I've set your status to AFK with the message `{message}`\n..however I cannot change your nickname to show you're AFK.")
        # # except CommandInvokeError as e:
        # #     print(e)
        
        # # Update the AFK users list
        # SemiFunc.update_afk(self.bot.logger)

class afkupdate(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="afkupdate", description="Update your AFK status!")
    async def afkupdate(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("It's normal to lose interest in life.. snowy has lost *ALL* interest in life...")
            return

        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.is_command_exception(ctx.author, "afk") or SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await afk_cmd(self, ctx, message, return_message)
            return
            
        if not SemiFunc.can_use_command(ctx, ctx.author, "staff"):
            await ctx.reply("That command is staff only.")
            return

async def setup(bot):
    await bot.add_cog(afkupdate(bot))
