###############################################
#
# File: cogs.temp.test.fakejoin
# Date: Around 09/04/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose: Test join message. Add the DM
#  message when they join.
# 
# Author: snow2code
#
###############################################


import os
import discord
import requests

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc
from utils.semibot import SemiBot

class Test__FakeJoin(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="fakejoin")
    async def fakejoin(self, ctx: Context, user: discord.Member):
        """
        Test the server join message

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        user: discord.Member
            The user to test with
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if SemiFunc.in_ignored_channel(ctx, "to_be_removed"):
            await ctx.reply("You can't use that command in this channel.")
            # await ctx.message.delete()
            return
        
        if not SemiFunc.can_use_command(ctx, ctx.author, "test"):
            await ctx.reply("That command is only usable by the bot dev for testing.")
            
        if user.bot == True:
            await ctx.reply("Join messages won't work on bots.")
            return
        
        # We have a code fork for Byte's Furry Helper bot.
        if self.bot.user.name == "Furry helper#5891" or self.bot.user.name == "Furry helper":
            pass
        else:
            before = ctx
            welcome_ping = before.guild.get_role( SemiFunc.get_role_id(before, "welcome_ping") )
            member, after = user, user

            # Welcome message
            if ctx.author.bot == False:
                # Make sure we have paths first!
                if not os.path.exists("assets/join_message_images"):
                    os.makedirs("assets/join_message_images")
                if not os.path.exists("assets/profile_pictures"):
                    os.makedirs("assets/profile_pictures")

                try:
                    response = requests.get(f"{member.display_avatar.url}", timeout=10)
                    response.raise_for_status()

                    img = Image.open(BytesIO(response.content))
                    img_resize = img.resize((128, 128))

                    img_resize.save(f"assets/profile_pictures/{member.name}.webp")

                    print("Downloaded and resized. Path: assets/profile_pictures/"+member.name+".webp")
                except requests.exceptions.RequestException as e:
                    self.bot.logger.warn(f"Error downloading {member.name}'s profile picture: {e}")
                except IOError as e:
                    self.bot.logger.warn(f"Error processing {member.name}'s profile picture: {e}")
                
                profile_picture = Image.open(f"assets/profile_pictures/{member.name}.webp").convert("RGBA")
                overlay = Image.open("assets/join_image_overlay.png").convert("RGBA")

                base = Image.new("RGBA", overlay.size)
                
                # (186, 85)
                base.paste(profile_picture, (186, 80), profile_picture)
                base.paste(overlay, (0, 0), overlay)

                # TEXT

                draw = ImageDraw.Draw(base)
                # font = ImageFont.truetype("assets/fonts/arial/ARIALBD 1.TTF", 20)
                font = ImageFont.truetype("assets/fonts/cambria-math/cambria-math.ttf", 20)
                font_italic = ImageFont.truetype("assets/fonts/arial/ARIALBI 1.TTF", 15)
                font_mem = ImageFont.truetype("assets/fonts/arial/ARIALBD 1.TTF", 15)

                bbox_mem = draw.textbbox((0,0), f'Member #{await SemiFunc.member_number(member.guild, member)}', font=font_mem)
                bbox_serv = draw.textbbox((0,0), member.guild.name, font=font)
                bbox_wel = draw.textbbox((0,0), f'Welcome {member.display_name}', font=font)
                bbox_to = draw.textbbox((0,0), f'to', font=font_italic)

                mem_width = bbox_mem[2] - bbox_mem[0]
                to_width = bbox_to[2] - bbox_to[0]
                serv_width = bbox_serv[2] - bbox_serv[0]
                wel_width = bbox_wel[2] - bbox_wel[0]
                x_mem = (base.width - mem_width) // 2
                x_wel = (base.width - wel_width) // 2
                x_ital = (base.width - to_width) // 2
                x_serv = (base.width - serv_width) // 2

                draw.text((x_mem, 60), f'Member #{await SemiFunc.member_number(member.guild, member)}', font=font_mem, fill=(255, 255, 255))
                draw.text((x_wel, 215), f'Welcome {member.display_name}', font=font, fill=(255, 255, 255))
                draw.text((x_ital, 235), f'to', font=font_italic, fill=(255, 255, 255))
                draw.text((x_serv, 255), member.guild.name, font=font, fill=(255, 255, 255))

                base.save(f"assets/join_message_images/{member.name}.png")


                ## Pedal to the metal! Send it!
                message = f"{welcome_ping.mention}"
                message = f"{message}\nWelcome {after.mention} to **{after.guild.name}**!"
                message = f"{message}\nGet roles in <#1418954294656499773>"
                message = f"{message}\n\nWe hope you'll have a wonderful stay here!"

                await ctx.send(content=message, file=discord.File(f"assets/join_message_images/{member.name}.png"))

                ## DM join message
                description = f"Welcome *{SemiBot.get_user_nick(ctx)['nick']}* to ***{ctx.guild.name}*** !\n\n"
                description += "Now you are here, follow these simple and short set of instructions:\n"
                description += "- Read the server rules - https://discord.com/channels/1414222707570118656/1414222708324958381\n"
                description += "- Verify - https://discord.com/channels/1414222707570118656/1419037577280880804 (reacting with ✅)\n\n"
                description += "We hope you'll have a wonderful and great stay here!"

                dm_embed = self.bot.create_embed(
                    title = "Welcome!",

                    description = description,

                    color = discord.Color.purple(),
                    use_by_snow2code_footer = True
                )

                dm_embed.set_image(url="attachment://join_image_overlay.png")

                await user.send(
                    file=discord.File("assets/join_image_overlay.png"),
                    embed=dm_embed
                )
            pass
        
        
async def setup(bot):
    await bot.add_cog(Test__FakeJoin(bot))
