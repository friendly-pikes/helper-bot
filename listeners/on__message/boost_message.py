###############################################
#
# File: listeners.on__message.boost_message
# Date: 05/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import os
import re
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

class BoostMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.type == discord.MessageType.premium_guild_subscription:
            boosts_channel = msg.guild.get_channel( SemiFunc.get_channel_id(msg, "boosts") )
            total_boosts = re.sub(r'0-9:!', '', boosts_channel.topic)
            total_boosts = boosts_channel.topic.replace("Thanks for the boosts! Total boosts: ", "")

            cur_boosts = msg.guild.premium_subscription_count
            total_boosts = int(total_boosts) + 1

            member = msg.author

            # to be safe cuz of that str error.. convert to int again
            # Optimised, I know. But it's better to be more safe than sorry.
            total_boosts = int(total_boosts)
            
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
            
            profile_picture = Image.open(f"assets/profile_pictures/{member.name}.webp").convert("RGBA")
            overlay = Image.open("assets/boost_image.png").convert("RGBA")

            base = Image.new("RGBA", overlay.size)
            boost_icon = Image.open("assets/boost.png").convert("RGBA")

            draw = ImageDraw.Draw(base)

            text = str(total_boosts)
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

            base.save(f"assets/boost_images/{member.id}_{total_boosts}.png")            
            await boosts_channel.send(files=[discord.File(f"assets/boost_images/{member.id}_{total_boosts}.png")])
            await boosts_channel.edit(topic=f"Thanks for the boosts! Total boosts: {total_boosts}")


async def setup(bot):
    await bot.add_cog(BoostMessage(bot))
