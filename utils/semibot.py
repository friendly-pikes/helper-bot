###############################################
#
# File: utils.semibot
# Date: 27/04/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import json
import random

from utils.custom.context import Context
from utils.files import files

def main_or_test(id: int):
    if id == 1414222707570118656:
        return "main"
    return "test"

class SemiBot():
    def __init__(*args, **kargs):
        super().__init__(*args, **kargs)

    def get_user_nick(ctx: Context):
        nick = ctx.author.display_name
        errors = []
            
        if ctx.author.nick != nick:
            if ctx.author.nick == None:
                nick = ctx.author.display_name
            else:
                nick = ctx.author.nick
        
        # 22/03/2026 - Prevent AFK status "stacking"
        if nick.find("[AFK]") >= 0:
            nick = nick.replace("[AFK] ", "")

        # Discord's nickname character limit is 32.
        if len(nick) > 26:
            # errors.append("I cannot put 'AFK' in your nickname because of character limits (32 max.)")
            errors.append("I cannot put 'AFK' in your nickname because of the nickname character limit. (32 max.)")
        
        # We can't change the server owner's nick.
        if ctx.author.id == ctx.guild.owner_id:
            errors.append("I cannot change your nickname.")

        return {"nick": nick, "errors": errors}


    def get_joke():
        with open(files.get_filepath("commands", "json"), "r", encoding="utf8") as file:
            config = json.load(file)

        selected_joke = random.choice(config['jokes'])
        
        return selected_joke