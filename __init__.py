from . import (
    classInstall,
    classSettings,
    classHandler,
    person,
    server,
    server_menu,
    databaseConfig,
    classweather
)

__all__ = [
    "classSettings",
    "classHandler",
    "person",
    "classInstall",
    "server",
    "server_menu",
    "databaseConfig",
    "classweather"
]


# --- Flask app creation ---
from flask import Flask

def create_app():
    frontend = Flask(__name__)

    # Import and register blueprints
    from .server import frontend
    frontend.register_blueprint(frontend)

    return frontend