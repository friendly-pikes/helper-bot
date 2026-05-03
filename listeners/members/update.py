###############################################
#
# File: listeners.members.update
# Date: 05/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import os
import requests
import discord

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from utils.discordbot import Bot
from utils.semifunc import SemiFunc

class OnMemberUpdated(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        if before.bot == False:
            verifiedid = SemiFunc.get_role_id(before, "verified")
            welcome_ping = before.guild.get_role( SemiFunc.get_role_id(before, "welcome_ping") )
            gen_chat = after.guild.get_channel( SemiFunc.get_channel_id(before, "general-chat") )
            member = after

            # Welcome message
            if before.get_role(verifiedid) == None and after.get_role(verifiedid):
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
                # message = f"{welcome_ping.mention}"
                # message = f"{message}\nWelcome {after.mention} to **{after.guild.name}**!"
                message = f"Welcome {after.mention} to **{after.guild.name}**!"
                message = f"{message}\nGet roles in <#1418954294656499773>"
                message = f"{message}\n\nWe hope you'll have a wonderful stay here!"

                await gen_chat.send(content=message, file=discord.File(f"assets/join_message_images/{member.name}.png"))
                
                # User @snowy 2.0 left from {server_name}
                # hope you had a wonderful stay sorry that you had to leave

            # Timeout
            # if before.timed_out_until or after.timed_out_until:
            #     before_timeout = before.timed_out_until
            #     after_timeout = after.timed_out_until
            #     print(f"before: {before_timeout.time()}\nafter: {after_timeout.time()}\n")
            #     if before_timeout is not None and after_timeout is None:
            #         print(f"{before.name} timeout has expired")
        
        
async def setup(bot):
    await bot.add_cog(OnMemberUpdated(bot))
