import json
import os

from utils.semifunc import *
from utils.custom.context import Context
# So we don't copy code 24/7 for diffrent files


def open_file(dir, filename, fileext):
    file = None
    filepath = os.path.abspath(f"{dir}/{filename}.{fileext}")

    with open(filepath, 'r', encoding='utf8') as raw:
        file = json.loads(raw.read())

    return file

def open_file_rawpath(path):
    file = None
    filepath = os.path.abspath(f"{path}")

    with open(filepath, 'r+', encoding='utf8') as raw:
        file = json.loads(raw.read())

    return file

def get_datafilepath(filename):
    filepath = os.path.abspath(f"data/{filename}.db")
    return filepath

def get_filepath(filename, fileext):
    filepath = os.path.abspath(f"misc/{filename}.{fileext}")
    return filepath

def get_config_entry(entry: str):
    return _config()[entry]

def get_bot_config_entry(entry: str):
    return _bot_config()[entry]

def get_users_config_entry(entry: str):
    return _users()[entry]


def _users():
    return open_file("misc", "users", "json")

def _bot_config():
    return open_file("misc", "bot", "json")

def _config():
    return open_file("misc", "config", "json")

def _banished():
    return open_file("misc", "banished", "json")

def _radar_ignore_force():
    return open_file("misc", "radar_forced_ignore", "json")

def _server_cfg():
    return open_file("misc", "server_cfg", "json")


def get_staff_commands():
    commands = open_file("misc", "commands", "json")
    return commands['staff']


def get_emoji_ids(guild_id):
    main_test = main_or_test(guild_id)
    return _server_cfg()['emoji_ids'][main_test]

def get_afk():
    afk = open_file("misc", "afk", "json")
    return afk['users']

def get_command_channel_ignores(ctx: Context, type: str, command: str):
    commands = open_file("misc", "commands", "json")
    main_test = main_or_test(ctx.guild.id)
    
    if commands['ignore_channels'][main_test][type] != None:
        if commands['ignore_channels'][main_test][type][command]:
            return commands['ignore_channels'][main_test][type][command]
        
    return []

def get_command_ignores():
    commands = open_file("misc", "commands", "json")
    return commands['ignores']

def get_channel_ids(guild_id: int):
    main_test = main_or_test(guild_id)
    return _server_cfg()['channel_ids'][main_test]

def get_role_ids(ctx: Context):
    main_test = main_or_test(ctx.guild.id)
    return _server_cfg()['role_ids'][main_test]


def get_channel_id(guild_id: int, name: str):
    return get_channel_ids(guild_id)[name]