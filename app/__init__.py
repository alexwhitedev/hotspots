from flask import Flask
from flask_restful import Api
import os

from app.api.errors import errors

app_api = Api()


def create_app():
    app = Flask(__name__)

    from app.api import bp as api_bp

    app_api.init_app(api_bp)
    app_api.errors = errors

    from app.api.routes import UserStat
    app_api.add_resource(UserStat, '/api/user_hotspots_stat/<stat_field>/user/<int:user_id>')

    app.register_blueprint(api_bp)

    return app
