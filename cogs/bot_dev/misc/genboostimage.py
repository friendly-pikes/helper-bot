###############################################
#
# File: cogs.bot_dev.misc.genboostimage
# Date: 30/04/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose: Command for generating a boost message.
#  Made for testing.
#  
# Author: snow2code
#
###############################################


import os
import time
import discord
import requests

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.custom.context import Context
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class ManagerCommands__Misc__GennBoost(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="genboostmsg")
    async def genboostmsg(self, ctx: Context, member: discord.Member, num: int):
        """
        Make a user's boost image

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        user: discord.Member
            The user to make a join image and message for
        num: int
            The boost amount
        """
        if SemiFunc.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
            
        if not SemiFunc.can_use_command(ctx, ctx.author, "bot_dev"):
            await ctx.reply("That command is only usable by the bot developer")
            return
        
        if not os.path.exists("assets/boost_images"):
            os.makedirs("assets/boost_images")
        if not os.path.exists("assets/profile_pictures"):
            os.makedirs("assets/profile_pictures")

        try:
            response = requests.get(f"{member.display_avatar.url}", timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            img_resize = img.resize((400, 400))

            img_resize.save(f"assets/profile_pictures/{member.name}.webp")

            # print("Downloaded and resized. Path: assets/profile_pictures/"+member.name+".webp")
        except requests.exceptions.RequestException as e:
            self.bot.logger.warn(f"Error downloading {member.name}'s profile picture: {e}")
        except IOError as e:
            self.bot.logger.warn(f"Error processing {member.name}'s profile picture: {e}")
        
        num = ctx.guild.premium_subscription_count
        
        time.sleep(0.5)
        profile_picture = Image.open(f"assets/profile_pictures/{member.name}.webp").convert("RGBA")
        overlay = Image.open("assets/boost_image.png").convert("RGBA")

        base = Image.new("RGBA", overlay.size)
        boost_icon = Image.open("assets/boost.png").convert("RGBA")

        draw = ImageDraw.Draw(base)

        text = str(num)
        font = ImageFont.truetype("assets/fonts/Noto_Sans_SC/NotoSansSC-SemiBold.ttf", 280)

        padding = 25

        # now we measure... i don't like measuring.....
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Grounded.
        grounded_x = 1860
        grounded_y = 870

        total_width = boost_icon.width + padding + text_w

        # start
        group_start_x = grounded_x - total_width // 2

        icon_x = group_start_x
        icon_y = grounded_y - boost_icon.height // 2

        text_x = icon_x + boost_icon.width + padding
        text_y = grounded_y - text_h // 2 - bbox[1]

        base.paste(profile_picture, (1657, 33), profile_picture)
        base.paste(overlay, (0, 0), overlay)
        base.paste(boost_icon, (icon_x, icon_y), boost_icon)

        # thin border
        draw.text((text_x-1, text_y), text, font=font, fill="black")
        draw.text((text_x+1, text_y), text, font=font, fill="black")
        draw.text((text_x, text_y-1), text, font=font, fill="black")
        draw.text((text_x, text_y+1), text, font=font, fill="black")

        # thicker border
        draw.text((text_x-5, text_y-5), text, font=font, fill="black")
        draw.text((text_x+5, text_y-5), text, font=font, fill="black")
        draw.text((text_x-5, text_y+5), text, font=font, fill="black")
        draw.text((text_x+5, text_y+5), text, font=font, fill="black")
        
        draw.text((text_x, text_y), text, font=font, fill="white")

        base.save(f"assets/boost_images/{member.name}_{num}.png")

        await ctx.send(files=[discord.File(f"assets/boost_images/{member.name}_{num}.png")])
        
async def setup(bot):
    await bot.add_cog(ManagerCommands__Misc__GennBoost(bot))

