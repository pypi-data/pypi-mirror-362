from flask import Blueprint

from . import __version__

bp = Blueprint("main", __name__)


@bp.route("/")
def main():
    return f"jbussdieker app v{__version__}"


@bp.route("/healthz")
def healthz():
    return "OK"
