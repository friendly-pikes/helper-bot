import os
import importlib

from flask import Blueprint, request
import web.app as app_module

api = Blueprint("api_private", __name__)

@api.route("/api/reload")
@api.route("/reload")
def reload_route():
    key = os.getenv('WEB_SECRET')

    if request.args.get("key") != key:
        return {"error": "You don't have the authorization to do that."}, 403
        
    app_module.reload_all()
    return {"status": "reloaded"}

@api.route("/api/clear")
@api.route("/clear")
def clear_output():
    key = os.getenv('WEB_SECRET')

    if request.args.get("key") != key:
        return {"error": "You don't have the authorization to do that."}, 403
        
    # os.system('cls' if os.name == 'nt' else 'clear')
    if os.name.lower() == "nt":
        os.system("clear")
    else:
        os.system("cls")
    print(os.name)
        
    return {"status": "Cleared output."}
        