import os
import json
import logging
import importlib
import dotenv

from flask import Flask, Response, send_from_directory, redirect, request
from werkzeug.serving import run_simple
from utils.discordbot import Bot

import web.routes.api as api_module
import web.routes.dashboard_api as dashboard_api_module
import web.routes.api_private as apiprivate_module
import web.misc_func as misc_module

dotenv.load_dotenv()

bot_instance: Bot = None
current_app = None
wrapper = None

def create_app():
    # app = Flask(__name__, template_folder="templates", static_folder="static")
    app = Flask(__name__, template_folder="templates", static_folder="s")

    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # no loggie
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.after_request
    def add_header(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    
    # @app.before_request
    # def force_https():
    #     if request.endpoint in app.view_functions and not request.is_secure:
    #         return redirect(request.url.replace("http://", "https://"))

    @app.route("/")
    def home():
        # return send_from_directory("", "index.html")


        # importlib.reload(misc_module)
        
        # return Response(
        #     json.dumps(misc_module.INFO, indent=4),
        #     mimetype="application/json"
        # )
        return Response(
            json.dumps(misc_module.INFO, indent=4),
            mimetype="application/json"
        )
    
    # @app.errorhandler(404)
    # def notfound(error):
    #     return send_from_directory("", "index.html")
    #     # return "hm"

    return app

# Register
def register(app: Flask):
    api_module.update(bot_instance)
    dashboard_api_module.update(bot_instance)
    
    app.register_blueprint(api_module.api)
    app.register_blueprint(apiprivate_module.api)


# Wrapper
class AppWrapper:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
    
# Reload shitty code
def reload_all():
    global current_app, wrapper, api_module, apiprivate_module

    print("Procedure beginning shortly...")
    
    importlib.reload(misc_module)

    if current_app != None:
        api_module = importlib.reload(api_module)
        apiprivate_module = importlib.reload(apiprivate_module)

        new_app = create_app()

        register(new_app)

        wrapper.app = new_app
        current_app = new_app

    print("Subject 2...")
    print("relative...")
    print("Success?")

# you better run.
def run():
    global current_app, wrapper

    port = int(os.environ.get("SERVER_PORT", 5000))

    current_app = create_app()
    register(current_app)

    wrapper = AppWrapper(current_app)

    ## HTTPS
    # run_simple("0.0.0.0", port, wrapper, ssl_context='adhoc')

    ## HTTP
    run_simple("0.0.0.0", port, wrapper)