from .factory import create_app


def register(subparsers):
    parser = subparsers.add_parser("app", help="Flask application")
    parser.add_argument("--host", default="0.0.0.0")
    parser.set_defaults(func=main)


def main(args):
    app = create_app()
    app.run("0.0.0.0", 9000)
