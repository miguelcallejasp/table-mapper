import src.main.model as model
import src.main.config as config
import src.main.routes as routes
import logging
from src.main.utils import utilities
from flask import Flask

app = Flask(__name__)


def start_flask_app():
    host = config.flask_app_host
    port = config.flask_app_port
    app.register_blueprint(routes.controller)
    app.run(host=host, port=port, debug=True)


def init():
    logging.warning("Starting Table Mapper Application")
    start_flask_app()


if __name__ == '__main__':
    init()
