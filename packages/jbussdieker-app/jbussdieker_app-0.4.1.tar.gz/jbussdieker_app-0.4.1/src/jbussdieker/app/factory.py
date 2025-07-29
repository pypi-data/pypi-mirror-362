from flask import Flask
from flask_bootstrap import Bootstrap5

from .blueprint import bp


def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    app.register_blueprint(bp)
    return app
