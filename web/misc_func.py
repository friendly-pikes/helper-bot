import json

from flask import Response
from utils.discordbot import Bot
from utils.database import Database

def leaderboard_Data(bot: Bot, value: int):
    user_data = Database.userdata_conn.cursor().execute(f"SELECT * FROM user_data ORDER BY tokens DESC").fetchall()
    leader = []

    for _user in user_data:
        if _user[0] > value:
            avatar = "https://cdn.discordapp.com/embed/avatars/0.png"
            user = bot.get_user(_user[1])

            # If we're testing bot, the user will be "None".. we have the main server database.
            if user != None:
                if user.avatar == None:
                    avatar = user.default_avatar.url
                else:
                    avatar = user.avatar.url
                
            leader.append({
                "avatar": avatar,
                "name": _user[2],
                "balance": _user[4]
            })

    return leader

## OTHER
def response_error(error_type, param, misc):
    if error_type == "required_param":
        return Response(
            json.dumps({
                "status": 400,
                "detail": f"Bad Request: Missing required parameter. Please provide {param} as a query parameter.",
                "errors": [
                    f"{param} is required"
                ]
            }, indent=4),
            mimetype="application/json"
        )
    elif error_type == "bad_param":
        return Response(
            json.dumps({
                "status": 400,
                "detail": f"Bad Parameter: {param} is a bad paramater for the endpoint.",
                "errors": [
                    f"{misc}"
                ]
            }, indent=4),
            mimetype="application/json"
        )
    
# Probably a better way to do this.. but eh.
INFO = {
    "message": "Fluffy Helper's Web API",
    "version": "1.1.0",
    "endpoints": {
        "public": {
            "POST /getLeaderboard": "Get the server leaderboard",
            "POST /banishCheck": "Check if something might get flagged or banished",
            "POST /getUsers": "Get users from the server and database",
            "POST /getJobs": "Get all jobs from the database"
        },
        "authenticated": {
            "POST /reload": "Reloads everything related to the web api",
            "POST /clear": "Clears the console"
        }
    }
}
            ## I used this as a example for my api help thing-
        # {
        #     "message": "Welcome to Glitchies API - Powered by Quantex",
        #     "version": "1.0.0",
        #     "endpoints": {
        #         "public": {
        #         "GET /user/getuser": "Get comprehensive user information",
        #         "GET /user/getuserheadshot": "Get user headshot URL",
        #         "GET /group/getgroup": "Get comprehensive group information"
        #         },
        #         "authenticated": {
        #         "POST /group/promote": "Promote user in group",
        #         "POST /group/demote": "Demote user in group",
        #         "POST /group/setrank": "Set user rank in group",
        #         "POST /group/shout": "Post group shout"
        #         }
        #     },
        #     "documentation": "See README or contact api@osoglitchy.com for detailed usage",
        #     "status": "operational"
        # }