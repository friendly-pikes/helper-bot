import sqlite3

from discord.ext import commands
from utils.custom.context import Context

import utils.files as files
from utils.discordbot import Bot
from utils.database import Database
from utils.semifunc import SemiFunc

class Banished(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        
    @commands.guild_only()
    @commands.hybrid_command(name="addbanisheduser")
    async def addbanisheduser(self, ctx: Context, id: int):
        """
        Add a user to the Banished User ID list.

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        id: int
            The user id to add to the banished user id list
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        cursor = Database.banished_conn.cursor()

        cursor.execute("SELECT * FROM banished_ids")
        resultRaw = cursor.fetchall()
        result = []
        
        for res in resultRaw:
            result.append(res[0])

        if id in result:
            await ctx.reply(f"The user id `{id}` is already in banished userids. It's a good idea not to have duplicates.", ephemeral=True)
        else:
            try:
                cursor.execute(f"INSERT INTO banished_ids VALUES ({id})")
                Database.banished_conn.commit()
                await ctx.reply(f"Successfully added the user id {id} to banished user ids!", ephemeral=True)
            except Exception as e:
                await ctx.reply(f"Unable to add the user id {id} to banished user ids.\n`{e}`")
        
    @commands.guild_only()
    @commands.hybrid_command(name="addbanishedbypass")
    async def addbanishedbypass(self, ctx: Context, bypass: str):
        """
        Add something to banished word bypasses

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        bypass: str
            The bypass to add (HAS TO HAVE no spaces AND HAS TO BE lower case)
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        cursor = Database.banished_conn.cursor()

        cursor.execute("SELECT * FROM banished_words_bypasses")
        resultRaw = cursor.fetchall()
        result = []
        
        for res in resultRaw:
            result.append(res[0])

        if bypass in result:
            await ctx.reply(f"The word `{bypass}` is already in banished word bypasses. It's a good idea not to have duplicates.", ephemeral=True)
        else:
            try:
                cursor.execute(f'INSERT INTO banished_words_bypasses VALUES ("{bypass}")')
                Database.banished_conn.commit()
                await ctx.reply(f"Successfully added `{bypass}` to banished word bypasses!", ephemeral=True)
            except Exception as e:
                await ctx.reply(f"Unable to add `{bypass}` to banished word bypasses.\n`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="addbanishedflag")
    async def addbanishedflag(self, ctx: Context, flag: str):
        """
        Add something to banished word flags

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        flag: str
            The flag message (HAS TO HAVE no spaces AND HAS TO BE lower case)
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
        
        cursor = Database.banished_conn.cursor()

        cursor.execute("SELECT * FROM banished_flagmsg")
        resultRaw = cursor.fetchall()
        result = []
        
        for res in resultRaw:
            result.append(res[0])

        if flag in result:
            await ctx.reply(f"The word `{flag}` is already in banished word bypasses. It's a good idea not to have duplicates.", ephemeral=True)
        else:
            try:
                cursor.execute(f'INSERT INTO banished_flagmsg VALUES ("{flag}")')
                Database.banished_conn.commit()
                await ctx.reply(f"Successfully added `{flag}` to banished word flags!", ephemeral=True)
            except Exception as e:
                await ctx.reply(f"Unable to add `{flag}` to banished word flags.\n`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="addbanishedwordall")
    async def addbanishedwordall(self, ctx: Context, word: str, *, message: str):
        """
        Add something to banished word for everyone

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        word: str
            The word (HAS TO HAVE no spaces AND HAS TO BE lower case)
        message: str
            The message that's sent when a user says that word
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        cursor = Database.banished_conn.cursor()

        cursor.execute("SELECT * FROM banished_words_noignore")
        resultRaw = cursor.fetchall()
        result = []
        
        for res in resultRaw:
            result.append(res[0])

        if word in result:
            await ctx.reply(f"The word `{word}` is already in banished words for everyone. It's a good idea not to have duplicates.", ephemeral=True)
        else:
            try:
                cursor.execute(f'INSERT INTO banished_words_noignore VALUES ("{word}", "{message}")')
                Database.banished_conn.commit()
                await ctx.reply(f"Successfully added `{word}` with the message `{message}` to banished words for everyone!", ephemeral=True)
            except Exception as e:
                await ctx.reply(f"Unable to add `{word}` to banished words for everyone.\n`{e}`")
        
    @commands.guild_only()
    @commands.hybrid_command(name="addbanishedword")
    async def addbanishedword(self, ctx: Context, word: str, *, message: str):
        """
        Add something to banished words

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        word: str
            The word (HAS TO HAVE no spaces AND HAS BE TO lower case)
        message: str
            The message that's sent when a user says the word.
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "manager"):
            await ctx.reply("That command is owners only.")
            return
        
        cursor = Database.banished_conn.cursor()

        cursor.execute("SELECT * FROM banished_words")
        resultRaw = cursor.fetchall()
        result = []
        
        for res in resultRaw:
            result.append(res[0])

        if word in result:
            await ctx.reply(f"The word `{word}` is already in banished words. It's a good idea not to have duplicates.", ephemeral=True)
        else:
            try:
                cursor.execute(f'INSERT INTO banished_words VALUES ("{word}", "{message}")')
                Database.banished_conn.commit()
                await ctx.reply(f"Successfully added `{word}` with the message `{message}` to banished words!", ephemeral=True)
            except Exception as e:
                await ctx.reply(f"Unable to add `{word}` with the message `{message}` to banished words.\n`{e}`")
    
async def setup(bot):
    await bot.add_cog(Banished(bot))
