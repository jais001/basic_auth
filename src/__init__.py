from flask import Flask

from src.views.user import user_auth_view_api
from src.api.user_auth_api import user_auth_apis
from src.config.config import Config
from src.core.extensions import db, jwt, limiter


def create_app():
    """Create a Flask app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_auth_view_api)
    app.register_blueprint(user_auth_apis)

    return app
