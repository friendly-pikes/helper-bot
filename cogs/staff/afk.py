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
        await ctx.reply("Cannot change your status to AFK because you've already used ?afk or /afk. Did you mean to use ?afkupdate?")
    else:
        conn = sqlite3.connect(f"misc/afk.db")
        cursor = conn.cursor()
        
        nick = ctx.author.display_name
        afkSince_createdat = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")

        if ctx.author.nick != nick:
            if ctx.author.nick == None:
                nick = ctx.author.display_name
            else:
                nick = ctx.author.nick

        cursor.execute(f'INSERT INTO users VALUES ("{nick}", {ctx.author.id}, {return_message}, "{message}", "{afkSince_createdat}")')
        conn.commit()
        conn.close()

        try:
            await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")
            await ctx.reply(f"I've set your status to AFK with the message `{message}`")
        except Forbidden as e:
            if e.text == "Missing Permissions":
                await ctx.reply(f"I've set your status to AFK with the message `{message}`\n..however I cannot change your nickname to show you're AFK.")
        # except CommandInvokeError as e:
        #     print(e)

        # Update the AFK users list
        SemiFunc.update_afk(self.bot.logger)

class afk(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="afk", description="Set your status to AFK!")
    async def afk(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        if SemiFunc.snowy_wants_to_die:
            await ctx.reply("You don't deserve me as a bot here, and you don't deserve Snowy here on earth....")
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
    await bot.add_cog(afk(bot))
