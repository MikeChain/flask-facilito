from flask import Flask
from .models import db


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(environment)

    return app
