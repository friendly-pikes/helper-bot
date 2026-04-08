import sqlite3
import discord

from utils.econ import Economy
from utils.database import Database
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class Econ__Work(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="work")
    async def work(self, ctx: Context, hours: int=7):
        """
        Do a shift at your job

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        hours: int
            The hours you want to work (2-9)
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        if Economy.econ__is_on_cooldown(ctx, ctx.author, self.bot.logger):
            await ctx.reply(f"You are on cooldown! Please try again tomorrow.")
            return
        ## Not fair.. we should do cooldown if they actually can work.
        # else:
        Economy.use_econ(ctx, ctx.author, self.bot.logger)

        jobs_conn = Database.jobs_conn
        cursor = jobs_conn.cursor()
        jobs = []

        for job in cursor.execute("SELECT * FROM jobs").fetchall():
            jobs.append([job[1], job[2]])

        user = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
        if len(user) > 0:
            job = user[3]
            for job_ in jobs:
                if job_[0] == job:
                    job = job_

            if user[3] == "NULL":
                await ctx.reply("You can't work if you don't have a job.")
            else:
                issues = []
                if hours > 10:
                    hours = 9
                    issues.append("You can work a maximum of 9 hours.")
                    
                wage = job[1] * hours
                bal = user[4]

                Database.userdata_conn.cursor().execute(f'UPDATE user_data SET tokens=? WHERE user_id=?', (bal + wage, ctx.author.id))
                Database.userdata_conn.commit()
                await ctx.reply(f"You went work for {job[0]} for {hours} hours, and earned {wage} {Economy.get_curreny_name()}!")
                Economy.econ__put_on_cooldown(ctx, ctx.author, self.bot.logger)

                if len(issues) > 0:
                    for issue in issues:
                        await ctx.send(f"-# {issue}")
        else:
            await ctx.reply("You aren't in our user database, so you aren't able to apply for a job right now.")

    @commands.guild_only()
    @commands.hybrid_command(name="quit")
    async def quit(self, ctx: Context):
        """
        Quit your current job

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        jobs_conn = Database.jobs_conn
        cursor = jobs_conn.cursor()
        jobs = []

        for job in cursor.execute("SELECT * FROM jobs").fetchall():
            jobs.append(job[1])

        user = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
        if len(user) > 0:
            # Make sure they have a job
            if user[3] in jobs:
                Database.userdata_conn.cursor().execute(f'UPDATE user_data SET job=? WHERE user_id=?', ("NULL", ctx.author.id))
                Database.userdata_conn.commit()

                await ctx.reply(f"Sad to see you leave {user[2]}. Thanks for working with and for us.")
        else:
            await ctx.reply("You aren't in our user database, so you aren't able to apply for a job right now.")

    @commands.guild_only()
    @commands.hybrid_command(name="apply")
    async def apply(self, ctx: Context, *, giv_job: str=""):
        """
        Apply for a job

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        gib_job: str
            The job name you want to apply for
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        if giv_job == "":
            await ctx.reply("You need to pass a job name as a argument, like: ?apply Test job\n-# Not case senstive")
            return
        

        jobs_conn = Database.jobs_conn
        cursor = jobs_conn.cursor()
        jobs = []

        for job in cursor.execute("SELECT * FROM jobs").fetchall():
            # Put the job in lower case because fuckery.
            jobs.append(job[1])

        user = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data WHERE user_id={ctx.author.id}").fetchone()
        if len(user) > 0:
            # "SNOWY THIS IS UNREALISTIC! YOU CAN HAVE MANY JOBS!"
            # Yea I know that, laddie. you can't save a whole list to a database.
            # So you can only apply for one job.
            # So sue me.. I ain't got shit you can take from me anyway... besides my foxes
            #    AND NOONE TAKES AWAY MY FOXES!!!!!

            # Make sure they don't already have a job
            if user[3] == None or user[3] == "NULL":

                # It should be a actual job we registered in the database.
                is_job = False
                
                for job in jobs:
                    if job.lower() == giv_job.lower():
                        is_job = True
                
                if is_job:
                    Database.userdata_conn.cursor().execute(f'UPDATE user_data SET job=? WHERE user_id=?', (job, ctx.author.id))
                    Database.userdata_conn.commit()

                    await ctx.reply(f"You've applied to work for {giv_job.lower()}, and got hired! Welcome to the team!")
                else:
                    await ctx.reply(f"It doesn't seem like {giv_job} is a job that exists in the database..")
            else:
                await ctx.reply(f"You already have a job or already work for {giv_job.lower()}.")
                    

        else:
            await ctx.reply("You aren't in our user database, so you aren't able to apply for a job right now.")

    @commands.guild_only()
    @commands.hybrid_command(name="jobs")
    async def jobs(self, ctx: Context):
        """
        List available jobs

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        embed:discord.Embed = Economy.econ_embed(title="")
        jobs_conn = Database.jobs_conn
        cursor = jobs_conn.cursor()

        cursor.execute("SELECT * FROM jobs")
        jobs_data = cursor.fetchall()

        description = "# Currently Available Jobs\n-# Note: Someone can have the same job as another person."
        fields = []

        for job in jobs_data:
            fields.append({
                "name": job[1],
                "value": f"£{job[2]} an hour",
                "inline": True
            })
        
        for field in fields:
            embed.add_field(name=field['name'],value=field['value'],inline=field['inline'])
        
        embed.description = description
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Econ__Work(bot))
