import os

from flask import Blueprint, request, jsonify
from utils.discordbot import Bot
from web.misc_func import *

api = Blueprint("dashboard_api", __name__)
bot: Bot = None

def update(bot_instance: Bot):
    global bot
    bot = bot_instance

def file_ext(file: str):
    file = file.lower()

    if file.endswith("html"):
        return "html"
    if file.endswith("py"):
        return "python"
    if file.endswith("log"):
        return "log"
    if file.endswith("env") or file.endswith("env.example"):
        return "dotenv"
    if file.endswith("gitattributes"):
        return "properties"
    if file.endswith("gitignore"):
        return "ignore"
    if file.endswith("md"):
        return "markdown"
    if file.endswith("json"):
        return "json"
    if file == "license":
        return "plaintext"
    return "unknown"

def sort_structure(path="."):
    entries = os.listdir(path)

    dirs = []
    files = []

    for entry in entries:
        if entry in ["__pycache__"]:
            continue

        full_path = os.path.join(path, entry)

        if os.path.isdir(full_path):
            dirs.append(entry)
        else:
            files.append(entry)
    
    return sorted(dirs, key=str.lower)+ sorted(files, key=str.lower)


@api.route("/getStructure", methods=["GET"])
def getStructure():
    key = os.getenv('WEB_SECRET')

    if request.args.get("key") != key:
        return {"error": "You don't have the authorization to do that."}, 403
    
    structure = {}
    for dir in sort_structure():
        if dir in [".git", ".github", ".local", ".trash", "assets", "data"]:
            continue
        
        add = file_ext(dir)

        if os.path.isdir(dir):
            add = {}

            for dir_a in sort_structure(dir):
                if dir_a == "__pycache__":
                    continue

                add[dir_a] = file_ext(dir_a)

                if os.path.isdir(f"{dir}/{dir_a}"):
                    add[dir_a] = {}
                    for dir_b in sort_structure(f"{dir}/{dir_a}"):
                        if dir_b == "__pycache__":
                            continue
                        if os.path.isdir(f"{dir}/{dir_a}/{dir_b}"):
                            add[dir_a][dir_b] = {}
                            for dir_c in sort_structure(f"{dir}/{dir_a}/{dir_b}"):
                                if dir_c == "__pycache__":
                                    continue
                                add[dir_a][dir_b][dir_c] = file_ext(dir_c)
                        else:
                            add[dir_a][dir_b] = file_ext(dir_b)
                else:
                    add[dir_a] = file_ext(dir_a)
        structure[dir] = add

    # return jsonify(structure)
    return Response(
        json.dumps(structure, indent=4),
        mimetype="application/json"
    )


@api.route("/getFileContent", methods=["GET"])
def getContent():
    key = os.getenv('WEB_SECRET')

    if request.args.get("key") != key:
        return {"error": "You don't have the authorization to do that."}, 403
    
    path = None
    # file_name = None

    if request.args.get("path"):
        path = request.args.get("path")
    else:
        return response_error("required_param", "path", None)

    # if request.args.get("file_name"):
    #     file_name = request.args.get("file_name")
    # else:
    #     return response_error("required_param", "file_name", None)


    # Main
    if os.path.exists(f"{path}"):
        file = open(f"{path}", "r", encoding="utf-8", errors="replace")
        content = json.dumps(file.read())
        return jsonify([content])
        # open(f"{path}/{file_name}", "r") as file:

        # print(test)

    return jsonify({"error": f"A file at {path} wasn't found."})

@api.route("/replaceFileContent", methods=["POST"])
def repalceFileContent():
    key = os.getenv('WEB_SECRET')

    if request.args.get("key") != key:
        return {"error": "You don't have the authorization to do that."}, 403
    print(request.args)
    path = request.args.get("path")
    content = request.args.get("content")
    # file_name = None

    if path == None:
        return response_error("required_param", "path", None)

    if content == None:
        return response_error("required_param", "content", None)
    print(content)

    # if request.args.get("file_name"):
    #     file_name = request.args.get("file_name")
    # else:
    #     return response_error("required_param", "file_name", None)


    # Main
    # if os.path.exists(f"{path}"):
    #     file = open(f"{path}", "r", encoding="utf-8", errors="replace")
    #     content = json.dumps(file.read())
    #     return jsonify([content])
    #     # open(f"{path}/{file_name}", "r") as file:

    #     # print(test)

    # return jsonify({"error": f"A file at {path} wasn't found."})
    return jsonify({})