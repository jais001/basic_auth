import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """COnfig
    """
    SECRET_KEY = 'basic_auth_flask_html'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '../users.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'tought_tight_flask_jwt_key_00007ey-fl'  # For encoding JWTs
