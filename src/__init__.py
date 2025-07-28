from flask import Flask

from src.views.auth import auth_blueprint
from src.config.config import Config
from src.core.models import db


def create_app():
    """Create a Flask app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_blueprint)

    return app
