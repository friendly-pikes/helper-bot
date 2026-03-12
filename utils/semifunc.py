import json
import discord
import random
import asyncio
import utils.files as files
from datetime import datetime

from utils.custom.context import Context
from utils.database import Database

def main_or_test(id: int):
    if id == 1414222707570118656:
        return "main"
    return "test"


class SemiFunc():
    def __init__(*args, **kargs):
        super().__init__(*args, **kargs)

    banished_ids = None
    banished_words_bypasses = None
    banished_flagmsg = None
    banished_words_noignore = None
    banished_words = None

    afk_users = None
    
    snowy_wants_to_die = True

    def update_banished(logger):
        data = Database.get_banished()

        SemiFunc.banished_ids = data['ids']
        SemiFunc.banished_words_bypasses = data['bypasses']
        SemiFunc.banished_flagmsg = data['flagmsg']
        SemiFunc.banished_words_noignore = data['noignore']
        SemiFunc.banished_words = data['words']
        
        logger.info("Updating banished lists.")

    def update_afk(logger):
        data = Database.get_afks()

        SemiFunc.afk_users = data['users']
        
        logger.info("Updating AFK Users.")

    def get_channel_id(ctx, channelname: str):
        channelids = files.get_channel_ids(ctx.guild.id)
        if channelids[channelname]:
            return channelids[channelname]
        return None
    
    def get_role_id(ctx: Context, rolename: str):
        roles = files.get_role_ids(ctx)

        if roles[rolename]:
            return roles[rolename]
        
        return None

    def can_use_command(ctx: Context, user: discord.Member, type: str):
        type = type.lower()
        config = files._config()
        # ignore_channels = []
        
        # try:
        #     ignore_channels = files.get_command_channel_ignores(ctx, type, ctx.command.name)
        # except Exception as e:
        #     ignore_channels = []
            
        #     if str(e) != "'Message' object has no attribute 'command'":
        #         print(f"error: {e}")

        # Before we do checks. we check if the channel is a ignore channel.
        # if ctx.channel.id in ignore_channels:
        #     return False
        
        if type == "owner":
            if user.id in config['owners']:
                return True
            return False
        elif type == "manager":
            if user.id in config['owners']:
                return True
            if user.id in config['managers']:
                return True
            return False
        elif type == "staff":
            role = SemiFunc.get_role_id(ctx, "staff")

            if user.get_role(role):
                return True
            return False
        elif type == "user":
            return True
        return False

    def is_command_exception(user: discord.User, cat: str):
        commands = files.get_filepath("commands", "json")

        with open(commands, "r", encoding="utf8") as file:
            data = json.load(file)
            expections = data['expections']

            if user.id in expections[cat]:
                return True
        return False

    async def member_number(guild: discord.Guild, member: discord.Member):
        # members = [m for m in guild.members if m.joined_at]
        # members.sort(key=lambda m: m.joined_at)

        # for i, m in enumerate(members, start=1):
        #     if m.id == member.id:
        #         return i
        
        # Better(?) - Let's be faster though..
        sorted_members = sorted(
            [m for m in guild.members if m.joined_at],
            key=lambda m: m.joined_at
        )

        return sorted_members.index(member) + 1


    async def moderate_user(bot, ctx: Context, user: discord.Member, moderation_type: str, args: []):
        moderation_embed = bot.create_embed_notitle()
        isGud = False

        
        if moderation_type == "kick":
            isGud = True
            moderation_embed.title = f"Staff at {files.get_server_name()}"
            moderation_embed.description = f"You've been kicked from {files.get_server_name()} by {ctx.author.name} ({ctx.author.display_name})"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}\n\n\nServer Invite: https://discord.gg/X8QqpeYgGF"
        elif moderation_type == "ban":
            isGud = True
            moderation_embed.title = f"Staff at {files.get_server_name()}"
            moderation_embed.description = f"You've been banned from {files.get_server_name()} permanently by {ctx.author.name} ({ctx.author.display_name})"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}\n\n\nServer Invite: https://discord.gg/X8QqpeYgGF"
        elif moderation_type == "mute":
            isGud = True
            moderation_embed.title = f"Staff at {files.get_server_name()}"
            moderation_embed.description = f"You've been muted in {files.get_server_name()} by {ctx.author.name} ({ctx.author.display_name})"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}"
        elif moderation_type == "unmute":
            isGud = True
            moderation_embed.title = f"Staff at {files.get_server_name()}"
            moderation_embed.description = f"You've been unmuted in {files.get_server_name()} by {ctx.author.name} ({ctx.author.display_name})"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}"
        elif moderation_type == "message_banished_flagged":
            audit = ctx.guild.get_channel(SemiFunc.get_channel_id(ctx, "audit"))

            # isGud = True
            moderation_embed.description = f"**Message sent by {ctx.author.mention} in {ctx.channel.mention} was flagged**"
            moderation_embed.description = moderation_embed.description + f"\n\nMessage: {ctx.content}\n"
            moderation_embed.description = moderation_embed.description + f"Detected flagged word: {args[1]}\n"
            moderation_embed.color = discord.Color.red()

            moderation_embed.timestamp = datetime.utcnow()
            moderation_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            moderation_embed.set_footer(text=f"Author: {user.id} | Message ID: {ctx.id}")
            
            # await ctx.reply(f"{args[0]}")
            await audit.send(embed=moderation_embed)

            return
        elif moderation_type == "message_banished":
            audit = ctx.guild.get_channel(SemiFunc.get_channel_id(ctx, "audit"))

            # isGud = True
            moderation_embed.description = f"**Message sent by {ctx.author.mention} in {ctx.channel.mention} was banished**"
            moderation_embed.description = moderation_embed.description + f"\n\nMessage: {ctx.content}\n"
            moderation_embed.description = moderation_embed.description + f"Detected banished word: {args[1]}\n"
            moderation_embed.color = discord.Color.red()

            moderation_embed.timestamp = datetime.utcnow()
            moderation_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            moderation_embed.set_footer(text=f"Author: {user.id} | Message ID: {ctx.id}")
            
            await ctx.reply(f"{args[0]}")
            await audit.send(embed=moderation_embed)

            return

        if isGud:
            await user.send(embed=moderation_embed)

    def get_inator_text(inator_type: str):
        inator_type = inator_type.lower()
        inator_text = f"{inator_type}inator"

        return inator_text

    async def pikesInator(bot, ctx: Context, user: discord.Member, inator_type:str, do_what: str):
        role_ids = files.get_role_ids(ctx)
        vanity_role_sep = SemiFunc.get_role_id(ctx, "vanity")
        role = SemiFunc.get_role_id(ctx, inator_type)
        inator_text = SemiFunc.get_inator_text(inator_type)

        embed = discord.Embed()

        if user.bot:
            await ctx.reply(f"I don't think {user.mention} has invoked or has been released from the {inator_text}")
        else:
            # Ignores
            if ctx.command:
                cmd = ctx.command.name.removeprefix("un")

                ignores = files.get_command_ignores()
                
                if ignores[cmd]:
                    if user.id in ignores[cmd]:
                        await ctx.reply(f"{user.mention} is not worthy of the {inator_text}.")
                        return
            # else:
            #     print(f"interaction {ctx.interaction.command.name}")

            if do_what == "remove":
                if inator_type == "explode":
                    await user.remove_roles(ctx.guild.get_role(role), reason=f"They unexploded")
                    await ctx.reply(f"{user.mention} has unexploded.. how.")
                else:
                    await user.remove_roles(ctx.guild.get_role(role), reason=f"They've been released from the {inator_text}")
                    await ctx.reply(f"{user.mention} has been released from the {inator_text}!")
            else:
                if user.get_role(role) == None:
                    if inator_type == "explode":
                        await user.add_roles(ctx.guild.get_role(role), reason=f"They exploded")
                        await ctx.reply("https://tenor.com/view/cat-explosion-sad-explode-gif-15295996165959499721")
                    else:
                        await user.add_roles(ctx.guild.get_role(role), reason=f"They invoked the {inator_text}")
                        await ctx.reply(f"{user.mention} has invoked of the wrath of the {inator_text}!")
                else:
                    await ctx.send(f"{user.mention} has already invoked of the wrath of the {inator_text}. They can't invoke the {inator_text} again.")
                
            await asyncio.sleep(1)

            ## If user doesn't have any vanity roles, remove the seperator
            if user.get_role(role_ids["cute"]) == None and user.get_role(role_ids["smol"]) == None and user.get_role(role_ids["explode"]) == None and user.get_role(role_ids["tall"]) == None:
                # safe guard cuz I'm just now adding vanity seperator to the code
                if user.get_role(vanity_role_sep):
                    await user.remove_roles(ctx.guild.get_role(vanity_role_sep), reason="No longer needs the seperator")
            else:
                await user.add_roles(ctx.guild.get_role(vanity_role_sep), reason="They need the seperator")

    async def pikesRadar(bot, user: discord.Member, radar: str):
        forced_ignore = files._radar_ignore_force()
        percent = random.randint(1, 100)
        embed = bot.create_embed(color=discord.Color.pink())

        emoji = "🎀"
        if radar == "gay":
            emoji = "🏳️‍🌈"


        # Ban 67.
        if percent == 67:
            if random.randint(1, 2) == 1:
                # Use 66
                percent = percent - 1
            else:
                # Use 69
                percent = percent + 2

        # If in ignore radars, set the percent to 0
        if user.id in forced_ignore['ignore'][radar]:
            percent = 0

        # If in forced radars, set the percent to 101
        if user.id in forced_ignore['forced'][radar]:
            percent = 101
        
        if radar == "silly":
            silly = SemiFunc.get_role_id(user, 'silly')

            # If radar is silly and the user has silly role, force sillie!
            if user.get_role(silly):
                percent = 100


        embed.title = f"{emoji} {radar.capitalize()} Radar {emoji}"
        
        if radar == "rizz":
            embed.description = f"{user.mention} has {percent}% {radar}! {emoji}"
        else:
            embed.description = f"{user.mention} is {percent}% {radar}! {emoji}"

        embed.color = discord.Color.pink()
        
        if radar == "cute":
            if percent >= 50 and percent < 80:
                embed.description = f"{embed.description}\n{user.name} is totally cute!"
            elif percent >= 80:
                embed.description = f"{embed.description}\n{user.name} is **A D O R A B L E**!"
        elif radar == "silly":
            if percent >= 50 and percent < 80:
                embed.description = f"{embed.description}\n{user.name} is totally silly!"
            elif percent >= 80:
                embed.description = f"{embed.description}\n{user.name} is **T O O  S I L L Y**!"
        elif radar == "gay" and percent >= 50:
            embed.description = f"{embed.description}\n{user.name} is totally gay!"
        
        embed.set_footer(text="Bot developed by snow2code")

        return embed
    
    def command_disabled(ctx: Context):
        commands = files.get_filepath("commands", "json")
        disabled = None

        with open(commands, "r", encoding="utf8") as file:
            data = json.load(file)
            disabled = data['disabled']

        if ctx.interaction == None:
            if ctx.command.name in disabled:
                return True
        else:
            if ctx.interaction.command.name in disabled:
                return True

        return False
    
    async def log_command_use(bot, author: discord.User, message_content, interaction: discord.Interaction, ctx: Context):
        if files.get_config_entry("output_on_command_used_enabled"):
            if interaction == None:
                bot.logger.info(msg=f"{author}: {message_content}")
            else:
                content = f"/{interaction.command.name}"
                
                for option in interaction.data["options"]:
                    content = f"{content} {option['name']}: {option['value']}"
                    # content = f"{content} {option['value']}"
                bot.logger.info(msg=f"{interaction.user.name}: {content}")
                if interaction.command.name in files.get_staff_commands():
                    audit = ctx.guild.get_channel(SemiFunc.get_channel_id(ctx, "audit"))
                    moderation_embed = bot.create_embed_notitle()

                    moderation_embed.description = f"Used `{interaction.command.name}` command in <#{ctx.channel.id}>"
                    moderation_embed.description = f"{moderation_embed.description}\n{content}"
                    moderation_embed.color = discord.Color.blue()

                    moderation_embed.timestamp = datetime.utcnow()
                    moderation_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

                    await audit.send(embed=moderation_embed)
                    # moderation_embed.set_footer(text=f"Bot developed by snow2code")
                    