import re
import json
import requests
import importlib

from flask import Blueprint, request, jsonify, Response
from utils.discordbot import Bot
from utils.database import Database
from utils.semifunc import SemiFunc
import web.misc_func as misc_module

api = Blueprint("api", __name__)
bot: Bot = None

def update(bot_instance: Bot):
    global bot
    bot = bot_instance

# Shorter stuff, then big stuff

@api.route("/botCredits", methods=["GET"])
def botCredits():
    
    return Response(
        json.dumps(misc_module.credits, indent=4),
        mimetype="application/json"
    )

@api.route("/getJobs", methods=["GET"])
def getJobs():
    return jsonify( Database.get_jobs()['jobs'] )

@api.route("/botStatus", methods=["GET"])
def botStatus():
    # If the web api is online, so is the bot.
    status = requests.get("https://discordstatus.com/api/v2/status.json")
    if status.ok:
        status = status.json()
        status = status["status"]["description"]
    
    return jsonify({"discord": {"status_provider": "discordstatus.com", "status": status}, "status": "online"})


@api.route("/getCommands", methods=['GET'])
def getCommands():
    if bot:
        commands = []
        for command in bot.commands:
            info = {}
            info["module"] = command.cog.__module__
            info["cog_name"] = command.cog_name
            info["command_name"] = command.name
            # info["command_arguments"] = command.clean_params
            if len(command.params) > 0:
                arguments = []
                for _param in command.params:
                    param = command.params[_param]
                    default = None
                    if param.default != param.empty:
                        default = param.default
                    arguments.append({"default": default, "name": param.name, "description": param.description, "required": param.required})
                # print(arguments)
                info["arguments"] = arguments
            # print(command.clean_params)

            commands.append(info)
        print()
        return jsonify(commands)
        
    return jsonify({"error": "Bot is inactive."})


@api.route("/getLeaderboard", methods=['GET'])
def getLeaderboard():
    leaderboard = []
    type = request.args.get("type")

    # we need "?type=whatever" in the url.
    if type == None:
        return misc_module.response_error("required_param", "type", None)
    else:
        # Check the type
        if type.lower() in ["used", "all"]:
            pass
        else:
            return misc_module.response_error("bad_param", "type", "Valid paramaters are: used and all")


    if type.lower() == "used":
        leaderboard = misc_module.leaderboard_Data(bot, 0)
    elif type.lower() == "all":
        leaderboard = misc_module.leaderboard_Data(bot, -1)

    return jsonify(leaderboard)

@api.route("/banishCheck", methods=["GET"])
def banishCheck():
    sentence = request.args.get("sentence")
    
    if sentence == None:
        return misc_module.response_error("required_param", "sentence", None)

    # Copied from listeners.on__message.banish_message out of laziness
    banished = SemiFunc.banished_words
    banished_nodelete = SemiFunc.banished_flagmsg
    banished_words_noignore = SemiFunc.banished_words_noignore
    banished_ignore = SemiFunc.banished_words_bypasses
    # banished_words_private = banished_words_privateA.private_banished()

    msg_content_lower = sentence.lower()
    content_lower_final = re.sub(r'[(#@-_\\/^,.)]', '', msg_content_lower)
    
    # Ignores
    for ignore in banished_ignore:
        if content_lower_final.find(ignore) >= 0:
            return jsonify({"status": "good", "detected": "", "message": "That will not get banished or flagged."})
    
    for thing in banished_nodelete:
        if content_lower_final.find(thing) >= 0:
            return jsonify({"status": "bad", "detected": thing, "message": f"That message would be flagged."})
    
    # Main course
    for banished_thing in banished:
        if content_lower_final.find(banished_thing) >= 0:
            print("banished")
            return jsonify({"status": "bad", "detected": banished_thing, "message": f"That message would be banished if not staff member."})
        
    for banished_thing in banished_words_noignore:
        if content_lower_final.find(banished_thing) >= 0:
            return jsonify({"status": "bad", "detected": banished_thing, "message": f"That message would be banished."})
    
    return jsonify({"status": "good", "detected": "", "message": "That will not get banished or flagged."})

@api.route("/getUsers", methods=["GET"])
def getUsers():
    user_data = Database.userdata_conn.execute(f"SELECT * FROM user_data").fetchall()
    users = []
    nicks = []

    for user in bot.get_all_members():
        if user.bot == False:
            can_add = True
            for nick_entry in nicks:
                if nick_entry['id'] == user.id:
                    can_add = False

            if can_add:
                nicks.append({
                    "id": user.id,
                    "nick": user.nick
                })

    for user in user_data:
        can_add = True

        for user_again in users:
            if user_again['userid'] == user[1]:
                can_add = False

        if can_add:
            job = user[3]
            display_name = None

            if job == "NULL" or job == None:
                job = "Unemployed"

            for nick_entry in nicks:
                if nick_entry['id'] == user[1]:
                    display_name = nick_entry['nick']
                    if display_name:
                        display_name = str(display_name).replace("[AFK] ", "")
                    break
                
            users.append({
                "username": user[2],
                "nick": display_name,
                "userid": user[1],
                "job": job,
                "credits": user[4]
            })

    return jsonify(users)