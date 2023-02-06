from flask import Flask


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(environment)

    return app
