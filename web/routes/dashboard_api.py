import os

from flask import Blueprint, request, jsonify
from utils.discordbot import Bot
from web.misc_func import *

api = Blueprint("dashboard_api", __name__)
bot: Bot = None

def update(bot_instance: Bot):
    global bot
    bot = bot_instance
